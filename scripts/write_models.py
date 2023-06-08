#!/usr/bin/env python

import sys

TABLE = """
<table>
  <tr align="center">
    <td rowspan="2" colspan="1"><b>Accession<br>code</b></td>
    <td rowspan="2" colspan="1"><b>Gene<br>name</b></td>
    <td colspan="3"><b>Active state</b></td>
    <td colspan="3"><b>Inactive state</b></td>
  </tr>
  <tr align="center">
    <td>Multi-state model</td>
    <td>Original AF2 model</td>
    <td>Best template<br>(seq. ID)</td>
    <td>Multi-state model</td>
    <td>Original AF2 model</td>
    <td>Best template<br>(seq. ID)</td>
  </tr>
  DATA</table>
"""

ADDR_BASE = "https://github.com/huhlim/odorant_receptors/blob/main/models"
PDB_BASE = "https://www.rcsb.org/structure"


def read_dat():
    data = {}
    with open("models/summary.dat") as fp:
        for line in fp:
            if line.startswith("#"):
                continue
            x = line.strip().split()
            name = x[0]
            data[name] = (x[2:6], x[7:12])
    return data


def main():
    data = read_dat()
    wrt_s = []
    for receptor, X in data.items():
        wrt = []
        wrt.append('<tr align="center">')
        accession_code, gene_name = receptor.split("_")
        wrt.append(
            f'  <td><a href="https://www.uniprot.org/uniprotkb/{accession_code}/entry">{accession_code}</a></td>'
        )
        if "OR" in gene_name:
            wrt.append(f"  <td>{gene_name}_HUMAN</td>")
        elif "hTAAR" in gene_name:
            wrt.append(f"  <td>{gene_name[1:]}_HUMAN</td>")
        elif "mTAAR" in gene_name:
            wrt.append(f"  <td>{gene_name[1:]}_MOUSE</td>")
        #
        wrt.append(
            f'  <td><a href="{ADDR_BASE}/{receptor}/{receptor}.active.pdb">{X[0][0]}</a></td>'
        )
        wrt.append(
            f'  <td><a href="{ADDR_BASE}/{receptor}/{receptor}.active.orig.pdb">{X[0][1]}</a></td>'
        )
        pdb_id = X[0][2].split("_")[0]
        wrt.append(f'  <td><a href="{PDB_BASE}/{pdb_id}">{X[0][2]}</a> ({X[0][3]}%)</td>')
        #
        wrt.append(
            f'  <td><a href="{ADDR_BASE}/{receptor}/{receptor}.inactive.pdb">{X[1][0]}</a></td>'
        )
        wrt.append(
            f'  <td><a href="{ADDR_BASE}/{receptor}/{receptor}.inactive.orig.pdb">{X[1][1]}</a></td>'
        )
        pdb_id = X[1][2].split("_")[0]
        wrt.append(f'  <td><a href="{PDB_BASE}/{pdb_id}">{X[1][2]}</a> ({X[1][3]}%)</td>')

        wrt.append("</tr>")
        for line in wrt:
            wrt_s.append(f"  {line}\n")
    #
    txt = "".join(wrt_s)
    #
    sys.stdout.write(TABLE.replace("DATA", txt))


if __name__ == "__main__":
    main()
