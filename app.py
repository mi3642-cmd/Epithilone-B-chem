import streamlit as st
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
import pandas as pd
import py3Dmol

st.set_page_config(page_title="Epothilone B Analyzer", layout="wide")

st.title("🧬 Epothilone B Stereochemistry Analyzer")

st.write("Analyze stereochemistry, chirality, and R/S configuration.")

smiles = "CC1=C[C@@H]2[C@@H](O)[C@H](OC(=O)C[C@H](C)[C@H](O)C(=O)N[C@@H](C)C(=O)O)[C@@H](O)[C@H](OC)[C@H](C)[C@@H](O)[C@H](C)C(=O)O[C@H]2O1"

if st.button("Analyze Molecule"):

    mol = Chem.MolFromSmiles(smiles)

    if mol:
        mol = Chem.AddHs(mol)
        Chem.AssignStereochemistry(mol, force=True)

        AllChem.EmbedMolecule(mol)
        AllChem.UFFOptimizeMolecule(mol)

        centers = Chem.FindMolChiralCenters(mol, includeUnassigned=False)

        st.subheader("🧪 Chiral Centers")

        data = []
        for idx, config in centers:
            atom = mol.GetAtomWithIdx(idx)
            st.write(f"Atom {idx} ({atom.GetSymbol()}): {config}")

            data.append({
                "Atom Index": idx,
                "Element": atom.GetSymbol(),
                "Configuration": config
            })

        st.success(f"Total chiral centers: {len(centers)}")

        st.dataframe(pd.DataFrame(data))

        # 2D drawing (safe version)
        drawer = rdMolDraw2D.MolDraw2DSVG(400, 400)
        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        svg = drawer.GetDrawingText()
        st.image(svg)

        # 3D viewer
        mol_block = Chem.MolToMolBlock(mol)

        view = py3Dmol.view(width=400, height=400)
        view.addModel(mol_block, "mol")
        view.setStyle({"stick": {}})
        view.setBackgroundColor("white")
        view.spin(True)
        view.zoomTo()

        st.subheader("🌐 3D View")
        st.components.v1.html(view._make_html(), height=400)

st.markdown("---")

st.write("### 📘 Concepts")
st.write("Stereochemistry: 3D arrangement of atoms")
st.write("Chirality: Non-superimposable mirror images")
st.write("R/S Configuration: Absolute configuration")

st.markdown("---")

st.write("### 👨‍🎓 Student Details")
st.write("Name: I MOHAMMED ABIDH")
st.write("Register Number: RA2511026050042")
st.write("Class: AIML - A")