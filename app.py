import streamlit as st
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
import py3Dmol

st.set_page_config(page_title="Epothilone B Analyzer", layout="wide")

# ===============================
# TITLE
# ===============================
st.title("🧬 Epothilone B Stereochemistry Analyzer")

# ===============================
# THEORY SECTION
# ===============================
st.header("🔍 What is Stereochemistry?")
st.write("""
Stereochemistry is the study of the 3D arrangement of atoms in molecules.
Even molecules with the same formula can behave differently depending on their spatial arrangement.
This is very important in pharmaceuticals.
""")

st.header("💊 About Epothilone B")
st.write("""
Epothilone B is a natural anticancer compound that stabilizes microtubules.
It is similar to Taxol and is used in cancer research.
Its biological activity depends strongly on its stereochemistry.
""")

st.header("🧪 What is R/S Configuration?")
st.write("""
R and S configurations describe how atoms are arranged around a chiral center:

- R (Rectus): clockwise arrangement
- S (Sinister): counterclockwise arrangement

These configurations affect how drugs interact with the human body.
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

    # ===============================
    # FIND CHIRAL CENTERS
    # ===============================
    centers = Chem.FindMolChiralCenters(mol, includeUnassigned=False)

    st.subheader("🧪 Chiral Centers (R/S Configuration)")

    chiral_atoms = []
    for idx, config in centers:
        atom = mol.GetAtomWithIdx(idx)
        st.write(f"Atom {idx} ({atom.GetSymbol()}): {config}")
        chiral_atoms.append(idx)

    st.success(f"Total chiral centers: {len(centers)}")

    # ===============================
    # 2D STRUCTURE WITH HIGHLIGHT
    # ===============================
    st.subheader("🧬 2D Structure (Highlighted Chiral Atoms)")

    drawer = rdMolDraw2D.MolDraw2DSVG(500, 400)
    drawer.DrawMolecule(mol, highlightAtoms=chiral_atoms)
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()

    st.components.v1.html(svg, height=400)

    # ===============================
    # 3D VIEW
    # ===============================
    st.subheader("🧪 3D Molecular View")

    mol_block = Chem.MolToMolBlock(mol)

    view = py3Dmol.view(width=600, height=400)
    view.addModel(mol_block, "mol")
    view.setStyle({"stick": {}})
    view.setBackgroundColor("white")
    view.spin(True)
    view.zoomTo()

    st.components.v1.html(view._make_html(), height=400)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown("### 👨‍🎓 Student Details")
st.write("Name: I MOHAMMED ABIDH")
st.write("Register Number: RA2511026050042")
st.write("Class: AIML - A")
