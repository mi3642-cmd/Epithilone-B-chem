import streamlit as st
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
import py3Dmol
import pandas as pd

st.set_page_config(page_title="Epothilone B Analyzer", layout="wide")

# ===============================
# TITLE (KEEP YOUR STYLE)
# ===============================
st.title("🧬 Epothilone B Stereochemistry Analyzer")

# ===============================
# THEORY (SAME STRUCTURE, BETTER TEXT)
# ===============================
st.header("🔬 What is Stereochemistry?")
st.write("""
Stereochemistry is the study of the three-dimensional arrangement of atoms in molecules.

Even if two molecules have the same molecular formula and bonding structure, their spatial arrangement can differ, leading to completely different chemical and biological behavior.

In pharmaceutical science:
- One stereoisomer may act as a drug
- Another may be inactive or harmful

This is because biological systems recognize molecules based on their 3D structure.
""")

st.header("💊 About Epothilone B")
st.write("""
Epothilone B is a natural anticancer compound derived from bacteria.

It stabilizes microtubules inside cells, preventing cancer cells from dividing.

Key points:
- Similar to Taxol
- Effective against drug-resistant cancers
- Activity depends strongly on stereochemistry

Its 3D structure is critical for its function.
""")

st.header("🧪 What is R/S Configuration?")
st.write("""
R/S configuration describes how atoms are arranged around a chiral center.

A chiral center is usually a carbon attached to four different groups.

Using CIP rules:
- R → Clockwise arrangement  
- S → Counterclockwise arrangement  

These configurations determine how a molecule interacts with biological systems.
""")

# ===============================
# ANALYSIS BUTTON
# ===============================
if st.button("🔬 Analyze Epothilone B"):

    smiles = "CC1=C[C@@H]2[C@@H](O)[C@H](OC(=O)C[C@H](C)[C@H](O)C(=O)N[C@@H](C)C(=O)O)[C@@H](O)[C@H](OC)[C@H](C)[C@@H](O)[C@H](C)C(=O)O[C@H]2O1"

    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    Chem.AssignStereochemistry(mol, force=True)

    AllChem.EmbedMolecule(mol)
    AllChem.UFFOptimizeMolecule(mol)

    centers = Chem.FindMolChiralCenters(mol, includeUnassigned=False)

    st.subheader("🧪 Chiral Centers")

    data = []
    chiral_atoms = []

    for idx, config in centers:
        atom = mol.GetAtomWithIdx(idx)
        symbol = atom.GetSymbol()

        st.write(f"Atom {idx} ({symbol}): {config}")

        data.append({
            "Atom Index": idx,
            "Element": symbol,
            "Configuration": config
        })

        chiral_atoms.append(idx)

    st.success(f"Total chiral centers: {len(centers)}")

    # ===============================
    # TABLE (NEW ADDITION)
    # ===============================
    st.subheader("📊 Chiral Centers Table")
    df = pd.DataFrame(data)
    st.dataframe(df)

    # ===============================
    # 2D STRUCTURE
    # ===============================
    st.subheader("🧬 2D Structure")

    drawer = rdMolDraw2D.MolDraw2DSVG(500, 400)
    drawer.DrawMolecule(mol, highlightAtoms=chiral_atoms)
    drawer.FinishDrawing()

    svg = drawer.GetDrawingText()
    st.components.v1.html(svg, height=400)

    # ===============================
    # 🔥 IMPROVED 3D VIEW
    # ===============================
    st.subheader("🌐 3D Structure (Enhanced View)")

    mol_block = Chem.MolToMolBlock(mol)

    view = py3Dmol.view(width=700, height=500)

    # Better visualization style
    view.addModel(mol_block, "mol")

    view.setStyle({
        "stick": {"radius": 0.2},
        "sphere": {"scale": 0.25}
    })

    # Highlight chiral atoms in RED
    for idx in chiral_atoms:
        view.addStyle(
            {"serial": idx},
            {"sphere": {"color": "red", "scale": 0.4}}
        )

    view.setBackgroundColor("white")
    view.zoomTo()
    view.spin(True)

    st.components.v1.html(view._make_html(), height=500)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.write("👨‍🎓 Name: I MOHAMMED ABIDH")
st.write("Register Number: RA2511026050042")
st.write("Class: AIML - A")
