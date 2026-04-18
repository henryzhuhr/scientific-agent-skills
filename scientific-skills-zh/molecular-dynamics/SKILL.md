---
name: molecular-dynamics
description: 使用 OpenMM 和 MDAnalysis 运行和分析分子动力学模拟。设置蛋白质/小分子系统，定义力场，运行能量最小化和生产MD，分析轨迹（RMSD、RMSF、接触图、自由能表面）。用于结构生物学、药物结合和生物物理学。
license: MIT
metadata:
    skill-author: Kuan-lin Huang
---

# 分子动力学

## 概述

分子动力学 (MD)模拟通过积分牛顿运动方程对分子系统的时间演化进行计算建模。该技能涵盖两个互补工具：

- **OpenMM** (https://openmm.org/)：具有 GPU 支持、Python API 和灵活力场支持的高性能 MD 仿真引擎
- **MDAnalysis** (https://mdanalysis.org/)：用于读取、写入和分析所有主要仿真的 MD 轨迹的 Python 库软件包

* *安装：**
```bash
conda install -c conda-forge openmm mdanalysis nglview
# or
pip install openmm mdanalysis
```

## 何时使用此技能

在以下情况下使用分子动力学：

- **蛋白质稳定性分析**：突变如何影响蛋白质动力学？
- **药物结合模拟**：表征药物的结合模式和停留时间配体
- **构象采样**：探索蛋白质灵活性和构象变化
- **蛋白质-蛋白质相互作用**：界面动力学和结合能量模型
- **RMSD/RMSF分析**：根据参考结构量化结构波动
- **自由能估计**：计算结合自由能或构象自由能
- **膜模拟**：脂质双层中的模型蛋白质
- **本质无序蛋白质**：研究IDR构象集合

## 核心工作流程：OpenMM模拟

### 1.系统准备

```python
from openmm.app import *
from openmm import *
from openmm.unit import *
import sys

def prepare_system_from_pdb(pdb_file, forcefield_name="amber14-all.xml",
                              water_model="amber14/tip3pfb.xml"):
    """
    Prepare an OpenMM system from a PDB file.

    Args:
        pdb_file: Path to cleaned PDB file (use PDBFixer for raw PDB files)
        forcefield_name: Force field XML file
        water_model: Water model XML file

    Returns:
        pdb, forcefield, system, topology
    """
    # Load PDB
    pdb = PDBFile(pdb_file)

    # Load force field
    forcefield = ForceField(forcefield_name, water_model)

    # Add hydrogens and solvate
    modeller = Modeller(pdb.topology, pdb.positions)
    modeller.addHydrogens(forcefield)

    # Add solvent box (10 Å padding, 150 mM NaCl)
    modeller.addSolvent(
        forcefield,
        model='tip3p',
        padding=10*angstroms,
        ionicStrength=0.15*molar
    )

    print(f"System: {modeller.topology.getNumAtoms()} atoms, "
          f"{modeller.topology.getNumResidues()} residues")

    # Create system
    system = forcefield.createSystem(
        modeller.topology,
        nonbondedMethod=PME,         # Particle Mesh Ewald for long-range electrostatics
        nonbondedCutoff=1.0*nanometer,
        constraints=HBonds,           # Constrain hydrogen bonds (allows 2 fs timestep)
        rigidWater=True,
        ewaldErrorTolerance=0.0005
    )

    return modeller, system
```

### 2.能量最小化

```python
from openmm.app import *
from openmm import *
from openmm.unit import *

def minimize_energy(modeller, system, output_pdb="minimized.pdb",
                     max_iterations=1000, tolerance=10.0):
    """
    Energy minimize the system to remove steric clashes.

    Args:
        modeller: Modeller object with topology and positions
        system: OpenMM System
        output_pdb: Path to save minimized structure
        max_iterations: Maximum minimization steps
        tolerance: Convergence criterion in kJ/mol/nm

    Returns:
        simulation object with minimized positions
    """
    # Set up integrator (doesn't matter for minimization)
    integrator = LangevinMiddleIntegrator(300*kelvin, 1/picosecond, 0.004*picoseconds)

    # Create simulation
    # Use GPU if available (CUDA or OpenCL), fall back to CPU
    try:
        platform = Platform.getPlatformByName('CUDA')
        properties = {'DeviceIndex': '0', 'Precision': 'mixed'}
    except Exception:
        try:
            platform = Platform.getPlatformByName('OpenCL')
            properties = {}
        except Exception:
            platform = Platform.getPlatformByName('CPU')
            properties = {}

    simulation = Simulation(
        modeller.topology, system, integrator,
        platform, properties
    )
    simulation.context.setPositions(modeller.positions)

    # Check initial energy
    state = simulation.context.getState(getEnergy=True)
    print(f"Initial energy: {state.getPotentialEnergy()}")

    # Minimize
    simulation.minimizeEnergy(
        tolerance=tolerance*kilojoules_per_mole/nanometer,
        maxIterations=max_iterations
    )

    state = simulation.context.getState(getEnergy=True, getPositions=True)
    print(f"Minimized energy: {state.getPotentialEnergy()}")

    # Save minimized structure
    with open(output_pdb, 'w') as f:
        PDBFile.writeFile(simulation.topology, state.getPositions(), f)

    return simulation
```

### 3. NVT 平衡

```python
from openmm.app import *
from openmm import *
from openmm.unit import *

def run_nvt_equilibration(simulation, n_steps=50000, temperature=300,
                            report_interval=1000, output_prefix="nvt"):
    """
    NVT equilibration: constant N, V, T.
    Equilibrate velocities to target temperature.

    Args:
        simulation: OpenMM Simulation (after minimization)
        n_steps: Number of MD steps (50000 × 2fs = 100 ps)
        temperature: Temperature in Kelvin
        report_interval: Steps between data reports
        output_prefix: File prefix for trajectory and log
    """
    # Add position restraints for backbone during NVT
    # (Optional: restraint heavy atoms)

    # Set temperature
    simulation.context.setVelocitiesToTemperature(temperature*kelvin)

    # Add reporters
    simulation.reporters = []

    # Log file
    simulation.reporters.append(
        StateDataReporter(
            f"{output_prefix}_log.txt",
            report_interval,
            step=True,
            potentialEnergy=True,
            kineticEnergy=True,
            temperature=True,
            volume=True,
            speed=True
        )
    )

    # DCD trajectory (compact binary format)
    simulation.reporters.append(
        DCDReporter(f"{output_prefix}_traj.dcd", report_interval)
    )

    print(f"Running NVT equilibration: {n_steps} steps ({n_steps*2/1000:.1f} ps)")
    simulation.step(n_steps)
    print("NVT equilibration complete")

    return simulation
```

### 4. NPT 平衡和生产

```python
def run_npt_production(simulation, n_steps=500000, temperature=300, pressure=1.0,
                        report_interval=5000, output_prefix="npt"):
    """
    NPT production run: constant N, P, T.

    Args:
        n_steps: Production steps (500000 × 2fs = 1 ns)
        temperature: Temperature in Kelvin
        pressure: Pressure in bar
        report_interval: Steps between reports
    """
    # Add Monte Carlo barostat for pressure control
    system = simulation.context.getSystem()
    system.addForce(MonteCarloBarostat(pressure*bar, temperature*kelvin, 25))
    simulation.context.reinitialize(preserveState=True)

    # Update reporters
    simulation.reporters = []
    simulation.reporters.append(
        StateDataReporter(
            f"{output_prefix}_log.txt",
            report_interval,
            step=True,
            potentialEnergy=True,
            temperature=True,
            density=True,
            speed=True
        )
    )
    simulation.reporters.append(
        DCDReporter(f"{output_prefix}_traj.dcd", report_interval)
    )

    # Save checkpoints
    simulation.reporters.append(
        CheckpointReporter(f"{output_prefix}_checkpoint.chk", 50000)
    )

    print(f"Running NPT production: {n_steps} steps ({n_steps*2/1000000:.2f} ns)")
    simulation.step(n_steps)
    print("Production MD complete")
    return simulation
```

## 轨迹分析MDAnalysis

### 1. 加载轨迹

```python
import MDAnalysis as mda
from MDAnalysis.analysis import rms, align, contacts
import numpy as np
import matplotlib.pyplot as plt

def load_trajectory(topology_file, trajectory_file):
    """
    Load an MD trajectory with MDAnalysis.

    Args:
        topology_file: PDB, PSF, or other topology file
        trajectory_file: DCD, XTC, TRR, or other trajectory
    """
    u = mda.Universe(topology_file, trajectory_file)
    print(f"Universe: {u.atoms.n_atoms} atoms, {u.trajectory.n_frames} frames")
    print(f"Time range: 0 to {u.trajectory.totaltime:.0f} ps")
    return u
```

### 2. RMSD 分析

```python
def compute_rmsd(u, selection="backbone", reference_frame=0):
    """
    Compute RMSD of selected atoms relative to reference frame.

    Args:
        u: MDAnalysis Universe
        selection: Atom selection string (MDAnalysis syntax)
        reference_frame: Frame index for reference structure

    Returns:
        numpy array of (time, rmsd) values
    """
    # Align trajectory to minimize RMSD
    aligner = align.AlignTraj(u, u, select=selection, in_memory=True)
    aligner.run()

    # Compute RMSD
    R = rms.RMSD(u, select=selection, ref_frame=reference_frame)
    R.run()

    rmsd_data = R.results.rmsd  # columns: frame, time, RMSD
    return rmsd_data

def plot_rmsd(rmsd_data, title="RMSD over time", output_file="rmsd.png"):
    """Plot RMSD over simulation time."""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(rmsd_data[:, 1] / 1000, rmsd_data[:, 2], 'b-', linewidth=0.5)
    ax.set_xlabel("Time (ns)")
    ax.set_ylabel("RMSD (Å)")
    ax.set_title(title)
    ax.axhline(rmsd_data[:, 2].mean(), color='r', linestyle='--',
               label=f'Mean: {rmsd_data[:, 2].mean():.2f} Å')
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    return fig
```

### 3. RMSF 分析（每个残基）灵活性）

```python
def compute_rmsf(u, selection="backbone", start_frame=0):
    """
    Compute per-residue RMSF (flexibility).

    Returns:
        resids, rmsf_values arrays
    """
    # Select atoms
    atoms = u.select_atoms(selection)

    # Compute RMSF
    R = rms.RMSF(atoms)
    R.run(start=start_frame)

    # Average by residue
    resids = []
    rmsf_per_res = []
    for res in u.select_atoms(selection).residues:
        res_atoms = res.atoms.intersection(atoms)
        if len(res_atoms) > 0:
            resids.append(res.resid)
            rmsf_per_res.append(R.results.rmsf[res_atoms.indices].mean())

    return np.array(resids), np.array(rmsf_per_res)
```

### 4. 蛋白质-配体接触

```python
def analyze_contacts(u, protein_sel="protein", ligand_sel="resname LIG",
                      radius=4.5, start_frame=0):
    """
    Track protein-ligand contacts over trajectory.

    Args:
        radius: Contact distance cutoff in Angstroms
    """
    protein = u.select_atoms(protein_sel)
    ligand = u.select_atoms(ligand_sel)

    contact_frames = []
    for ts in u.trajectory[start_frame:]:
        # Find protein atoms within radius of ligand
        distances = contacts.contact_matrix(
            protein.positions, ligand.positions, radius
        )
        contact_residues = set()
        for i in range(distances.shape[0]):
            if distances[i].any():
                contact_residues.add(protein.atoms[i].resid)
        contact_frames.append(contact_residues)

    return contact_frames
```

## 力场选择指南

|系统|推荐力场|水模型|
|--------------------|------------------------|-------------|
|标准蛋白| AMBER14 (`amber14-all.xml`) | TIP3P-FB |
|蛋白质+小分子|琥珀14 + GAFF2 | TIP3P-FB |
|膜蛋白|魅力36米| TIP3P |
|核酸| AMBER99-bsc1 或 AMBER14 | TIP3P |
|蛋白质紊乱 | ff19SB 或 CHARMM36m | TIP3P |

## 系统准备工具

### PDBFixer（用于原始 PDB 文件）

```python
from pdbfixer import PDBFixer
from openmm.app import PDBFile

def fix_pdb(input_pdb, output_pdb, ph=7.0):
    """Fix common PDB issues: missing residues, atoms, add H, standardize."""
    fixer = PDBFixer(filename=input_pdb)
    fixer.findMissingResidues()
    fixer.findNonstandardResidues()
    fixer.replaceNonstandardResidues()
    fixer.removeHeterogens(True)    # Remove water/ligands
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    fixer.addMissingHydrogens(ph)

    with open(output_pdb, 'w') as f:
        PDBFile.writeFile(fixer.topology, fixer.positions, f)

    return output_pdb
```

### 用于小分子的 GAFF2（通过 OpenFF 工具包）

```python
# For ligand parameterization, use OpenFF toolkit or ACPYPE
# pip install openff-toolkit
from openff.toolkit import Molecule, ForceField as OFFForceField
from openff.interchange import Interchange

def parameterize_ligand(smiles, ff_name="openff-2.0.0.offxml"):
    """Generate GAFF2/OpenFF parameters for a small molecule."""
    mol = Molecule.from_smiles(smiles)
    mol.generate_conformers(n_conformers=1)

    off_ff = OFFForceField(ff_name)
    interchange = off_ff.create_interchange(mol.to_topology())
    return interchange
```

## 最佳实践

- **始终在 MD 之前最小化**：原始 PDB 结构存在空间冲突
- **生产前平衡**：NVT (50–100 ps) → NPT (100–500 ps) → 生产
- **使用 GPU**：GPU 上的模拟速度提高 10–100 倍(CUDA/OpenCL)
- **具有 HBonds 约束的 2 fs 时间步**：标准；使用 4 fs 和 HMR（氢质量重新分配）
- **仅分析平衡轨迹**：丢弃前 20–50% 作为平衡
- **保存检查点**：MD 运行可能会失败；检查点允许重新启动
- **周期性边界条件**：溶剂化系统所需
- **静电PME**：比带电系统的截止方法更准确

## 其他资源

- **OpenMM文档**：https://openmm.org/documentation.html
- **MDAnalysis用户指南**： https://docs.mdanalysis.org/
- **GROMACS**（替代MD引擎）：https://manual.gromacs.org/
- **NAMD**（替代）：https://www.ks.uiuc.edu/Research/namd/
- **CHARMM-GUI**（基于Web的系统构建器）： https://charmm-gui.org/
- **AmberTools**（免费 Amber 工具）：https://ambermd.org/AmberTools.php
- **OpenMM 论文**：Eastman P 等人。 (2017) PLOS 计算生物学。 PMID：28278240
- **MD分析论文**：Michaud-Agrawal N等人。 （2011）计算化学杂志。 PMID：21500218
