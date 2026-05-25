# Product Modality Taxonomy

## 1. Purpose

This document defines the standard product modality taxonomy for the Pharmaceutical Regulatory and Clinical Intelligence System.

It replaces the narrower concept of a biologics-only taxonomy and supports broader regulatory and clinical trial intelligence across:

- Small molecule drugs
- Peptide drugs
- Oligonucleotide and nucleic acid drugs
- Biologics
- Antibody-based products
- Antibody-drug conjugates
- Vaccines
- Cell therapies
- Gene therapies
- Radiopharmaceuticals
- Combination products
- Other or uncertain therapeutic modalities

This taxonomy is used by:

- Regulatory update classification
- Clinical trial search and filtering
- Company-by-indication pipeline tracking
- MCP tool parameters
- Claude report generation
- Future classifier implementation

This file is a classification governance document. It is not a regulatory guideline, CMC development manual, or clinical strategy document.

---

## 2. Classification Principles

### 2.1 Use Standard Labels

All source ingestion, classifiers, MCP tools, and Claude workflows should use the standard labels defined in this document.

Do not create new labels casually.

### 2.2 Classify Conservatively

If the modality cannot be confidently identified, use:

```text
unknown
```

or

```text
requires_manual_review
```

Do not force classification based only on weak keywords.

### 2.3 Preserve Source Terms

When a source uses its own product description, preserve the original source term in a separate field.

Recommended fields:

```text
source_product_description
standard_modality
standard_submodality
classification_confidence
classification_notes
```

### 2.4 Allow Multiple Modalities When Needed

Some products may legitimately belong to more than one modality.

Examples:

- Antibody-drug conjugate: antibody + cytotoxic payload
- Peptide-drug conjugate: peptide + small molecule payload
- Cell therapy with gene modification: cell therapy + gene therapy
- Radioligand therapy: targeted ligand + radioisotope
- Device-drug combination: drug + device

For such cases, use:

```text
primary_modality
secondary_modalities
```

### 2.5 Do Not Over-Classify

The taxonomy should support practical filtering and reporting. It should not become an excessively detailed encyclopedia.

Highly specific subtypes should only be added when they are useful for:

- Regulatory update tracking
- Clinical trial comparison
- CMC impact assessment
- MCP filtering
- Claude report generation

---

## 3. Standard Top-Level Labels

The following top-level labels are approved.

| Standard Label | Description |
|---|---|
| `small_molecule` | Conventional or targeted chemically synthesized drugs |
| `peptide` | Synthetic or recombinant peptide-based drugs |
| `oligonucleotide` | ASO, siRNA, miRNA, aptamer, and related nucleic acid therapeutics |
| `mrna_rna` | mRNA or RNA-based drug products, including RNA vaccines where appropriate |
| `antibody` | Monoclonal antibodies, bispecific antibodies, antibody fragments, Fc-fusion products when antibody-like |
| `adc` | Antibody-drug conjugates |
| `recombinant_protein` | Recombinant proteins, enzymes, cytokines, hormones, fusion proteins |
| `biosimilar` | Biosimilar and interchangeable biosimilar products |
| `vaccine` | Prophylactic or therapeutic vaccines |
| `cell_therapy` | Autologous, allogeneic, immune cell, stem cell, and other cell-based therapies |
| `gene_therapy` | In vivo or ex vivo gene therapies, including viral and non-viral vectors |
| `plasma_derived` | Plasma-derived proteins and blood-derived therapeutic products |
| `microbiome_live_biotherapeutic` | Live biotherapeutic products and microbiome-based therapeutics |
| `radiopharmaceutical` | Diagnostic or therapeutic products containing radioisotopes |
| `combination_product` | Product combining drug, biologic, device, or diagnostic components |
| `other_modality` | Product modality is known but does not fit current standard labels |
| `unknown` | Product modality cannot be determined from available source data |
| `requires_manual_review` | Classification is ambiguous and requires human review |

---

## 4. MVP v1 Supported Categories

MVP v1 should support the following categories only:

```text
small_molecule
peptide
oligonucleotide
mrna_rna
antibody
adc
recombinant_protein
biosimilar
vaccine
cell_therapy
gene_therapy
radiopharmaceutical
combination_product
unknown
requires_manual_review
```

MVP v1 should avoid over-detailed subclassification. Submodality may be recorded when obvious, but core filtering should remain at the top-level label.

---

## 5. v2 and v3 Expansion Plan

### 5.1 v2 Expansion

v2 may add more detailed submodality support for:

```text
bispecific_antibody
antibody_fragment
fc_fusion
enzyme_replacement_therapy
glp_1_receptor_agonist
protac
molecular_glue
peptide_drug_conjugate
plasma_derived
microbiome_live_biotherapeutic
```

### 5.2 v3 Expansion

v3 may add:

```text
Chinese / Japanese / European terminology mapping
NMPA / PMDA-specific modality terminology
More detailed vector taxonomy
More detailed vaccine platform taxonomy
More detailed radiopharmaceutical taxonomy
More detailed combination product classification
```

Do not add v2 or v3 categories into MVP v1 workflows unless explicitly approved.

---

## 6. Full Taxonomy

### 6.1 Small Molecule

Standard label:

```text
small_molecule
```

Approved sublabels:

```text
conventional_small_molecule
targeted_small_molecule
kinase_inhibitor
protease_inhibitor
hormone_small_molecule
immunomodulator
protac
molecular_glue
```

Common keywords:

```text
small molecule
chemical entity
NCE
new chemical entity
kinase inhibitor
JAK inhibitor
BTK inhibitor
EGFR inhibitor
ALK inhibitor
PARP inhibitor
protease inhibitor
PROTAC
molecular glue
```

Classification notes:

- Use `small_molecule` for chemically synthesized drugs that are not peptides, oligonucleotides, radiopharmaceuticals, or conjugates.
- Do not classify peptides as small molecules unless the source explicitly describes the product as a small molecule and there is no better information.
- PROTACs and molecular glues may be classified as small molecule unless future workflows require a separate top-level category.

---

### 6.2 Peptide

Standard label:

```text
peptide
```

Approved sublabels:

```text
synthetic_peptide
recombinant_peptide
peptide_hormone
cyclic_peptide
glp_1_receptor_agonist
peptide_drug_conjugate
cell_penetrating_peptide
```

Common keywords:

```text
peptide
synthetic peptide
peptide hormone
GLP-1
GLP-1 receptor agonist
cyclic peptide
peptide conjugate
peptide-drug conjugate
```

Classification notes:

- Use `peptide` for therapeutic products primarily defined by peptide sequence or peptide structure.
- GLP-1 receptor agonists may be classified as `peptide` when the product is peptide-based.
- Peptide-drug conjugates should use `peptide` as primary modality and `combination_product` or payload type as secondary modality when needed.
- Do not classify large recombinant proteins as peptide unless the product is clearly described as a peptide drug.

---

### 6.3 Oligonucleotide

Standard label:

```text
oligonucleotide
```

Approved sublabels:

```text
antisense_oligonucleotide
siRNA
miRNA
aptamer
splice_switching_oligonucleotide
oligonucleotide_conjugate
```

Common keywords:

```text
ASO
antisense oligonucleotide
siRNA
small interfering RNA
miRNA
microRNA
aptamer
splice switching
oligonucleotide
RNA interference
RNAi
GalNAc conjugate
```

Classification notes:

- Use `oligonucleotide` for short nucleic acid therapeutics such as ASO, siRNA, miRNA, aptamers, and related products.
- If the product is mRNA-based, use `mrna_rna` instead.
- Oligonucleotide conjugates should retain the primary modality as `oligonucleotide`.

---

### 6.4 mRNA / RNA-Based Products

Standard label:

```text
mrna_rna
```

Approved sublabels:

```text
mrna_therapeutic
mrna_vaccine
self_amplifying_rna
circular_rna
rna_vaccine
```

Common keywords:

```text
mRNA
messenger RNA
self-amplifying RNA
saRNA
circular RNA
RNA vaccine
mRNA vaccine
```

Classification notes:

- Use `mrna_rna` for mRNA or RNA-based therapeutic and vaccine products.
- If the product is primarily a vaccine, `vaccine` may be added as a secondary modality.
- If the product is a short oligonucleotide such as ASO or siRNA, use `oligonucleotide` instead.

---

### 6.5 Antibody

Standard label:

```text
antibody
```

Approved sublabels:

```text
monoclonal_antibody
bispecific_antibody
multispecific_antibody
antibody_fragment
nanobody
fc_fusion
immune_checkpoint_antibody
```

Common keywords:

```text
monoclonal antibody
mAb
bispecific antibody
multispecific antibody
antibody fragment
Fab
scFv
nanobody
Fc fusion
checkpoint inhibitor
anti-PD-1
anti-PD-L1
anti-CTLA-4
```

Classification notes:

- Use `antibody` for antibody-based products that are not ADCs.
- If an antibody is conjugated to a cytotoxic payload, radioisotope, or other active payload, consider `adc`, `radiopharmaceutical`, or `combination_product` as appropriate.
- Fc-fusion products may be classified as `antibody` or `recombinant_protein` depending on project needs. For consistency, use `antibody` when the Fc component is central to the product design.

---

### 6.6 Antibody-Drug Conjugate

Standard label:

```text
adc
```

Approved sublabels:

```text
cytotoxic_adc
immune_stimulating_adc
radioimmunoconjugate
```

Common keywords:

```text
ADC
antibody-drug conjugate
antibody drug conjugate
payload
linker
DAR
drug-antibody ratio
```

Classification notes:

- Use `adc` when an antibody is conjugated to a drug payload.
- Preserve payload information when available, but do not create excessive payload-specific labels unless needed.
- If the antibody is conjugated to a radioisotope, classify as `radiopharmaceutical` with `antibody` as secondary modality, or use `adc` only if the source explicitly describes it as ADC.

---

### 6.7 Recombinant Protein

Standard label:

```text
recombinant_protein
```

Approved sublabels:

```text
enzyme
enzyme_replacement_therapy
cytokine
growth_factor
hormone_protein
fusion_protein
coagulation_factor_recombinant
```

Common keywords:

```text
recombinant protein
enzyme
enzyme replacement therapy
ERT
cytokine
interferon
interleukin
growth factor
recombinant hormone
fusion protein
coagulation factor
```

Classification notes:

- Use `recombinant_protein` for large therapeutic proteins produced through recombinant expression.
- Do not classify antibody-based products here unless the product is better understood as a fusion protein rather than an antibody.
- Peptide hormones should usually be classified under `peptide` if they are peptide-based rather than large recombinant proteins.

---

### 6.8 Biosimilar

Standard label:

```text
biosimilar
```

Approved sublabels:

```text
biosimilar
interchangeable_biosimilar
follow_on_biologic
```

Common keywords:

```text
biosimilar
interchangeable biosimilar
follow-on biologic
biosimilarity
reference product
```

Classification notes:

- Use `biosimilar` when the source explicitly describes the product as a biosimilar or interchangeable biosimilar.
- The reference product modality may be captured separately when available.
- Do not infer biosimilar status only because the product has the same target or mechanism as another biologic.

---

### 6.9 Vaccine

Standard label:

```text
vaccine
```

Approved sublabels:

```text
prophylactic_vaccine
therapeutic_vaccine
mrna_vaccine
viral_vector_vaccine
protein_subunit_vaccine
inactivated_vaccine
live_attenuated_vaccine
dna_vaccine
cancer_vaccine
```

Common keywords:

```text
vaccine
prophylactic vaccine
therapeutic vaccine
mRNA vaccine
viral vector vaccine
protein subunit vaccine
inactivated vaccine
live attenuated vaccine
DNA vaccine
cancer vaccine
```

Classification notes:

- Use `vaccine` for products intended to induce immune protection or therapeutic immune response.
- If the vaccine platform is mRNA, viral vector, DNA, or protein-based, add platform information as a sublabel or secondary modality.
- Do not classify immune checkpoint antibodies as vaccines.

---

### 6.10 Cell Therapy

Standard label:

```text
cell_therapy
```

Approved sublabels:

```text
CAR_T
TCR_T
NK_cell_therapy
tumor_infiltrating_lymphocyte
stem_cell_therapy
dendritic_cell_therapy
autologous_cell_therapy
allogeneic_cell_therapy
gene_modified_cell_therapy
```

Common keywords:

```text
cell therapy
CAR-T
CAR T
TCR-T
NK cell
TIL
tumor infiltrating lymphocyte
stem cell
dendritic cell
autologous
allogeneic
gene-modified cell
```

Classification notes:

- Use `cell_therapy` for products where living cells are the therapeutic product.
- If the cells are genetically modified, add `gene_therapy` as a secondary modality when relevant.
- Do not classify non-cellular biologics as cell therapy merely because they act on immune cells.

---

### 6.11 Gene Therapy

Standard label:

```text
gene_therapy
```

Approved sublabels:

```text
in_vivo_gene_therapy
ex_vivo_gene_therapy
AAV_gene_therapy
lentiviral_vector_gene_therapy
adenoviral_vector_gene_therapy
non_viral_gene_therapy
gene_editing
CRISPR_based_therapy
base_editing
prime_editing
```

Common keywords:

```text
gene therapy
AAV
adeno-associated virus
lentiviral vector
adenoviral vector
gene editing
CRISPR
base editing
prime editing
in vivo gene therapy
ex vivo gene therapy
```

Classification notes:

- Use `gene_therapy` for products intended to introduce, modify, replace, or edit genetic material.
- Genetically modified cell therapies should usually use `cell_therapy` as primary modality and `gene_therapy` as secondary modality.
- Do not classify mRNA therapeutics as gene therapy unless the source explicitly does so.

---

### 6.12 Plasma-Derived Product

Standard label:

```text
plasma_derived
```

Approved sublabels:

```text
immunoglobulin
albumin
coagulation_factor_plasma_derived
plasma_protein
antithrombin
```

Common keywords:

```text
plasma-derived
human plasma
immunoglobulin
IVIG
albumin
coagulation factor
factor VIII
factor IX
antithrombin
```

Classification notes:

- Use `plasma_derived` for products derived from human plasma.
- Recombinant coagulation factors should be classified as `recombinant_protein`, not `plasma_derived`.

---

### 6.13 Microbiome / Live Biotherapeutic

Standard label:

```text
microbiome_live_biotherapeutic
```

Approved sublabels:

```text
live_biotherapeutic_product
microbiome_therapy
fecal_microbiota_product
engineered_microbe
```

Common keywords:

```text
live biotherapeutic
LBP
microbiome
microbiota
fecal microbiota
engineered microbe
bacterial therapeutic
```

Classification notes:

- Use this category for live microorganisms or microbiome-derived therapeutic products.
- Do not classify antibiotics or small molecule anti-infectives as microbiome therapies.

---

### 6.14 Radiopharmaceutical

Standard label:

```text
radiopharmaceutical
```

Approved sublabels:

```text
radioligand_therapy
radioimmunotherapy
diagnostic_radiopharmaceutical
therapeutic_radiopharmaceutical
alpha_emitter
beta_emitter
PET_tracer
SPECT_tracer
```

Common keywords:

```text
radiopharmaceutical
radioligand
radioisotope
radioimmunotherapy
Lutetium-177
Lu-177
Actinium-225
Ac-225
Iodine-131
PET tracer
SPECT tracer
alpha emitter
beta emitter
```

Classification notes:

- Use `radiopharmaceutical` when the product contains a radioisotope for diagnostic or therapeutic use.
- If the targeting ligand is an antibody or peptide, capture that as a secondary modality.
- Do not classify non-radioactive imaging agents as radiopharmaceutical unless they contain a radioactive component.

---

### 6.15 Combination Product

Standard label:

```text
combination_product
```

Approved sublabels:

```text
drug_device_combination
biologic_device_combination
drug_diagnostic_combination
drug_biologic_combination
device_assisted_delivery
```

Common keywords:

```text
combination product
drug-device combination
prefilled syringe
autoinjector
drug-device
companion diagnostic
device-assisted delivery
```

Classification notes:

- Use `combination_product` when the product combines drug, biologic, device, or diagnostic components in a way relevant to regulatory or clinical tracking.
- Delivery devices such as prefilled syringes or autoinjectors should not automatically change the primary modality unless the combination aspect is central to the regulatory issue.
- Companion diagnostics should be captured when relevant to trial or regulatory intelligence.

---

## 7. Ambiguous Case Handling

### 7.1 Unknown Modality

Use:

```text
unknown
```

when the source does not provide enough information to identify product modality.

### 7.2 Requires Manual Review

Use:

```text
requires_manual_review
```

when the source suggests multiple possible modalities and automated classification may be misleading.

Examples:

- Product described only by code name
- Trial lists an intervention but no description
- Product uses a platform term without clear modality
- Product appears to combine cell and gene therapy
- Product appears to be a conjugate but payload or targeting component is unclear
- Translated source terms are ambiguous

### 7.3 Multiple Modalities

Use the following structure when multiple modalities are present:

```yaml
primary_modality: cell_therapy
secondary_modalities:
  - gene_therapy
standard_submodality: CAR_T
classification_confidence: high
classification_notes: Genetically modified CAR-T product.
```

### 7.4 Confidence Levels

Recommended confidence labels:

```text
high
medium
low
requires_manual_review
```

Use `low` or `requires_manual_review` when classification is based on limited keywords.

---

## 8. Do Not Over-Classify Rule

Do not create new modality labels for:

- Every target
- Every mechanism of action
- Every payload
- Every vector serotype
- Every linker type
- Every disease area
- Every regulatory pathway
- Every dosage form

Targets, mechanisms, payloads, indications, and dosage forms should be stored in separate fields when needed.

The modality taxonomy should answer:

```text
What kind of therapeutic product is this?
```

It should not try to answer:

```text
What is the product target?
What is the mechanism of action?
What is the indication?
What is the formulation?
What is the regulatory pathway?
```

---

## 9. Relationship to Other Documents

This taxonomy supports and should be referenced by:

```text
PROJECT_INSTRUCTION.md
README.md
docs/mcp_tool_contract.md
docs/data_dictionary.md
workflows/regulatory_clinical_intelligence_workflow.md
```

The previous planned file name:

```text
docs/biologics_taxonomy.md
```

should not be used as the primary taxonomy file because the project scope includes small molecule drugs, peptide drugs, and other non-biologic modalities.

---

## 10. Maintenance Rule

This document must be updated before:

1. Adding a new product modality filter to MCP tools
2. Adding a new classifier label
3. Adding a new report filter based on modality
4. Adding a new source-specific mapping for modality terms
5. Adding Chinese, Japanese, or European terminology mappings
6. Splitting one top-level modality into multiple top-level categories
7. Deprecating or renaming an existing modality label

When updating this document, avoid breaking existing labels unless absolutely necessary.

If a label must be renamed, provide a migration note.

---

## 11. Current Build Instruction

For MVP v1, implement only the approved top-level labels listed below:

```text
small_molecule
peptide
oligonucleotide
mrna_rna
antibody
adc
recombinant_protein
biosimilar
vaccine
cell_therapy
gene_therapy
radiopharmaceutical
combination_product
unknown
requires_manual_review
```

Do not implement advanced submodality classification until the MVP v1 workflow is stable.

