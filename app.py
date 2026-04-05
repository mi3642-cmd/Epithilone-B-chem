import streamlit as st
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
import py3Dmol
import pandas as pd

st.set_page_config(page_title="Epothilone B Dashboard", layout="wide")

# ===============================
# UI + BUTTON FIX
# ===============================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: #eef2f7;
}

/* TEXT FIX */
h1, h2, h3, h4, h5 {
    color: #1f3c88 !important;
}

p, li, div {
    color: #111 !important;
}

/* TITLE */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #1f3c88;
}

/* CARDS */
.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
}

/* BUTTON FIX */
.stButton>button {
    background-color: #1f3c88;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background-color: #162d66;
    color: white;
}

/* HIGHLIGHT */
.highlight {
    color: #ff4d6d;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# HEADER
# ===============================
st.markdown("<div class='title'>🧬 Epothilone B Molecular Dashboard</div>", unsafe_allow_html=True)
st.write("")

# ===============================
# TOP CARDS
# ===============================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🔬 Stereochemistry")
    st.write("Study of 3D structure of molecules affecting drug behavior.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 💊 Epothilone B")
    st.write("Anticancer compound that stabilizes microtubules.")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🧪 R/S Configuration")
    st.write("Describes spatial arrangement of atoms around chiral centers.")
    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# CONTENT (YOUR TEXT)
# ===============================
st.markdown("## 📘 Detailed Explanation")

st.markdown("""
### 🔬 What is Stereochemistry?
Stereochemistry is the study of the three-dimensional arrangement of atoms in molecules.

Even if two molecules have the same molecular formula and bonding structure, their spatial arrangement can differ, leading to completely different chemical and biological behavior.

In pharmaceutical science:
- One stereoisomer may act as a drug  
- Another may be inactive or harmful  

This is because biological systems recognize molecules based on their 3D structure.

---

### 💊 About Epothilone B
Epothilone B is a natural anticancer compound derived from bacteria.

It stabilizes microtubules inside cells, preventing cancer cells from dividing.

Key points:
- Similar to Taxol  
- Effective against drug-resistant cancers  
- Activity depends strongly on stereochemistry  

Its 3D structure is critical for its function.

---

### 🧪 What is R/S Configuration?
R/S configuration describes how atoms are arranged around a chiral center.

A chiral center is usually a carbon attached to four different groups.

Using CIP rules:
- R → Clockwise arrangement  
- S → Counterclockwise arrangement  

These configurations determine how a molecule interacts with biological systems.
""")

# ===============================
# ANALYSIS
# ===============================
st.markdown("## 🔬 Molecular Analysis")

if st.button("Analyze Epothilone B"):

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

        st.markdown(f"<span class='highlight'>Atom {idx} ({symbol}) → {config}</span>", unsafe_allow_html=True)

        data.append({
            "Atom Index": idx,
            "Element": symbol,
            "Configuration": config
        })

        chiral_atoms.append(idx)

    st.success(f"Total chiral centers: {len(centers)}")

    # TABLE
    st.subheader("📊 Chiral Centers Table")
    df = pd.DataFrame(data)
    st.dataframe(df)

    # VISUALS
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧬 2D Structure")

        drawer = rdMolDraw2D.MolDraw2DSVG(400, 400)
        drawer.DrawMolecule(mol, highlightAtoms=chiral_atoms)
        drawer.FinishDrawing()

        svg = drawer.GetDrawingText()
        st.components.v1.html(svg, height=400)

    with col2:
        st.subheader("🌐 3D Structure")

        mol_block = Chem.MolToMolBlock(mol)

        view = py3Dmol.view(width=600, height=400)
        view.addModel(mol_block, "mol")

        view.setStyle({
            "stick": {"radius": 0.2},
            "sphere": {"scale": 0.3}
        })

        for idx in chiral_atoms:
            view.addStyle({"serial": idx}, {"sphere": {"color": "red", "scale": 0.4}})

        view.setBackgroundColor("white")
        view.spin(True)
        view.zoomTo()

        st.components.v1.html(view._make_html(), height=400)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.write("👨‍🎓 Name: I. MOHAMMED ABIDH")
st.write("Register Number: RA2511026050042")
st.write("Class: AIML - A")
