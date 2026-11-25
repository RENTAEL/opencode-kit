# Software R&D: Frascati Rules for Informatics

## Primary rule

Software development is an innovation-related activity that sometimes incorporates R&D. A software project is R&D only when its completion depends on a scientific and/or technological advance **and** its aim is the systematic resolution of scientific and/or technological uncertainty.  
**Frascati basis:** Chapter 2, §2.68, p. 67.

## What can qualify

- Software that is an end product or embedded in one can be R&D when the R&D criteria apply.  
  **Frascati basis:** Chapter 2, §2.69, p. 67.
- A software component can qualify when it produces an advance in computer software. Incremental advances can qualify; a change need not be revolutionary. Using software for a new application/purpose alone is not an advance.  
  **Frascati basis:** Chapter 2, §2.70, pp. 67-68.
- Listed examples include new operating systems/languages, original-technology search engines, re-engineering to resolve hardware/software conflicts, new or more efficient algorithms based on new techniques, and original encryption/security techniques.  
  **Frascati basis:** Chapter 2, §2.71, p. 68.

## R&D type in computer and information sciences

Frascati gives its own worked example for this field, which can be used to place a thesis on the basic/applied/experimental-development axis:

- **Basic research:** research on the properties of general algorithms for handling large amounts of real-time data.
- **Applied research:** research to reduce spam by understanding the structure or business model of spam, what spammers do, and their motivations.
- **Experimental development:** a start-up takes code developed by researchers and develops the business case for the resulting software product for improved on-line marketing.

**Frascati basis:** Chapter 2, §2.40, p. 57.

## Routine exclusions

The following are not R&D when routine or based on already available advances:

- Business applications/information systems built with known methods and existing tools.
- Adding user functionality, including basic data entry.
- Websites or software made with existing tools.
- Standard encryption, security verification, and data-integrity testing.
- Product customisation, unless it adds knowledge that significantly improves the base program.
- Routine debugging/maintenance, except qualifying work before experimental development ends.

**Frascati basis:** Chapter 2, §2.72, p. 68.

## Project boundary

A collection of individually non-R&D systems projects can generate technological uncertainty at a larger-project level. Conversely, a large project that adopts available technologies for a commercial product may contain no R&D except for discrete additional R&D elements needed for integration.  
**Frascati basis:** Chapter 2, §2.73, p. 68.

## Data, big-data, benchmarking, and demonstration boundaries

- General-purpose or routinely collected data are not R&D merely because they are later analysed. Data collection, processing, and interpretation can be R&D when they are specially undertaken for a scientific project, or when the project develops new methods for those activities.  
  **Frascati basis:** Chapter 2, §2.90, p. 72.
- A big-data project is R&D only if it meets all five criteria, including a clearly identified original knowledge gap and resources focused on it. Tools that facilitate reproducibility are R&D only when explicitly part of the project objectives and budget; otherwise they are dissemination.  
  **Frascati basis:** Chapter 2, §2.93, pp. 73-74.
- Standard testing and benchmarking are not R&D; devising new or substantially improved testing methods can be R&D.  
  **Frascati basis:** Chapter 2, §2.92, p. 73.
- A prototype can fall within R&D while it collects evidence essential to an R&D project; ordinary copies after satisfactory testing are excluded. User demonstrations are not R&D, while technical demonstration integral to an R&D project can be.  
  **Frascati basis:** Chapter 2, §2.50 and Table 2.3, pp. 62-63; §§2.100-2.101, pp. 75-76.
- A feasibility study using existing techniques before implementation is not R&D; feasibility work on a research project is part of R&D.  
  **Frascati basis:** Chapter 2, §2.114, p. 79.

## Activities excluded from R&D

Chapter 2, §2.8 lists activities that are closely linked to R&D but must be excluded from R&D measurement. These are common misattributions in Informatics theses.

- Scientific and technical information services — collecting, coding, recording, classifying, disseminating, translating, analysing, and evaluating by bibliographic/patent/advisory services and conferences — are excluded, unless conducted solely or primarily for R&D support or within an R&D project.  
  **Frascati basis:** Chapter 2, §§2.111-2.112, p. 78.
- Testing and standardisation — maintaining national standards, calibrating secondary standards, and the routine testing and analysis of materials, components, products, or processes — are not R&D.  
  **Frascati basis:** Chapter 2, §2.113, p. 79.
- Specialised health care — the routine investigation and normal application of specialised medical knowledge — is usually not R&D; an R&D element may exist when carried out, for example, in university hospitals.  
  **Frascati basis:** Chapter 2, §2.115, p. 79.
- Policy-related studies and activities that provide close support to policy actions (policy advice, media relations, legal advice, public relations, administrative technical support) are excluded. Research that gives decision makers a thorough knowledge of social, economic, or natural phenomena is included.  
  **Frascati basis:** Chapter 2, §§2.116-2.118, pp. 79-80.
- Programmatic evaluations and intelligence/evidence-building for policy or programme advice are not automatically R&D; assess the expertise involved, how knowledge is codified, and how methodology quality is assured. There is a significant risk that socio-economic consultancy is inaccurately presented as R&D.  
  **Frascati basis:** Chapter 2, §2.119, p. 80.

## S2 Informatics interpretation for datasets and benchmarks

- “We created a dataset” is not a sufficient contribution. State the original knowledge gap and what method, evidence, or scientific question the dataset enables.
- “We benchmarked models” is not a sufficient contribution. Establish whether the protocol tests an unaddressed question, controls confounders, and yields transferable evidence beyond a leaderboard.
- “We built a prototype/demo” is not a sufficient contribution. Identify the uncertainty it tests and the evidence it contributes before it becomes a deployment artifact.

## S2 Informatics interpretation

Use the following as diagnostic prompts, not as quotations from Frascati:

| Claim to test | Evidence required |
|---|---|
| “We use AI.” | Identify the advance/uncertainty, not the library or model name. |
| “We built a framework.” | Define the original mechanism, competing approaches, hypotheses, and tests; packaging is not enough. |
| “We fine-tuned a model.” | Specify what unknown is investigated and why the adaptation/method yields transferable knowledge. |
| “We deploy at the edge.” | Establish the unresolved resource/accuracy/robustness trade-off and compare against feasible baselines. |
| “We use a new dataset.” | Show whether it supports a new generalisable finding, not just a local demonstration. |

## Safe wording

- “The software artifact may support an R&D project; R&D status depends on the advance, uncertainty, and all five criteria.”
- “This is potentially implementation-oriented because the proposed activity currently resembles a listed routine exclusion; stronger evidence could change that assessment.”
- “The proposed method may be an incremental software advance, but that is not established until the comparison and uncertainty are specified.”
