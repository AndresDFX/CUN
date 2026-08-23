# Anchored Formative Feedback in Google Docs Without Full-Drive Access: A Documented API Limitation and a Session-Based Workaround with Export Verification

**Retroalimentación formativa anclada en Google Docs sin acceso total a Drive: una limitación documentada de la API y una solución basada en sesión con verificación por exportación**

---

**Corresponding author**

Julian Andrés Castaño Espinosa
School of Engineering, Corporación Unificada Nacional de Educación Superior — CUN
Bogotá, Colombia
julian_castanoe@cun.edu.co
ORCID: https://orcid.org/0009-0003-6598-432X

**Authorship.** Single author, who designed, implemented and operated the system reported.

**Institutional affiliation of the work:** School of Engineering, CUN. Internal research call
CUN 2026 — Thematic Research Groups, Phase II.

---

## ABSTRACT

Formative feedback is more useful when it is attached to the sentence it refers to than when it
arrives as a separate list of remarks. In Google Docs — the platform on which a large share of
student writing in Latin American higher education is produced and shared — attaching feedback to a
specific phrase programmatically turns out to be harder than the API surface suggests. We report
three findings established while building a feedback tool for five university courses. First, the
Drive API exposes a writable `anchor` field on comments, but Google's own documentation states that
Workspace editors render developer-defined anchored comments **as unanchored**, so the field is
writable and cosmetically ineffective. Second, no "comment-only" OAuth scope exists: commenting on a
document owned by someone else requires the full `drive` scope, which grants read and write access
to the instructor's entire Drive — a disproportionate privacy cost for a feedback tool. Third, the
suggestion mode that instructors actually ask for is absent from the API entirely. We then describe
the workaround adopted: driving the editor through the instructor's existing browser session, which
requires no new authorisation grant, and verifying every published comment by exporting the document
and checking for `w:commentRangeStart` and `w:commentRangeEnd` markers in the resulting archive
rather than by reading the screen. We report the operational safeguards this required, including an
incident in which comments were published to a real student document and had to be withdrawn, and we
state plainly what the approach does not solve. No student data are reported and no learning outcome
is claimed.

**Keywords:** formative feedback, Google Docs API, OAuth scopes, educational technology, browser
automation, privacy by design, higher education, negative result

## RESUMEN

La retroalimentación formativa es más útil cuando va pegada a la frase de la que habla que cuando
llega como una lista aparte. En Google Docs —la plataforma en la que se escribe y se comparte buena
parte de la producción estudiantil en la educación superior latinoamericana— anclar
programáticamente un comentario a una frase resulta más difícil de lo que sugiere la superficie de
la API. Reportamos tres hallazgos establecidos al construir una herramienta de retroalimentación
para cinco asignaturas universitarias. Primero: la API de Drive expone un campo `anchor` escribible,
pero la propia documentación de Google indica que los editores de Workspace muestran los comentarios
anclados definidos por el desarrollador **como no anclados**, de modo que el campo se escribe y no
surte efecto visual. Segundo: no existe un alcance OAuth de «solo comentar»; comentar un documento
ajeno exige el alcance completo `drive`, que concede lectura y escritura sobre todo el Drive del
docente. Tercero: el modo sugerencia que los docentes piden no existe en la API. Describimos después
la solución adoptada —conducir el editor con la sesión de navegador que el docente ya tiene, sin
pedir ninguna autorización nueva— y la verificación de cada comentario publicado exportando el
documento y comprobando las marcas `w:commentRangeStart` y `w:commentRangeEnd`, en lugar de mirar la
pantalla. Reportamos las salvaguardas que esto exigió, incluido un incidente en el que se publicaron
comentarios en el documento real de un estudiante y hubo que retirarlos, y decimos con claridad qué
no resuelve el enfoque.

**Palabras clave:** retroalimentación formativa, API de Google Docs, alcances OAuth, tecnología
educativa, automatización de navegador, privacidad por diseño, educación superior, resultado negativo

---

## 1. INTRODUCTION

Written formative feedback works better when the student can see which sentence provoked it. This is
not a controversial claim; it follows from the basic requirement that feedback be specific enough to
act on. In practice, at scale, instructors often abandon specificity: a document with forty pages
receives a summary paragraph, because attaching thirty separate remarks to thirty separate phrases by
hand is slow.

The obvious response is to automate the attaching. Google Docs is where much of this writing lives,
it has a comment system with an anchor concept, and it has a public API. The expectation is that a
short program can read the document, decide what to say, and attach each remark to its phrase.

This report documents why that expectation fails, what the failure costs in privacy terms, and what
we did instead. It is offered as a **negative result with a workaround**: the kind of finding that is
rarely published, frequently rediscovered, and expensive to rediscover.

## 2. THE THREE FINDINGS

### 2.1 The anchor field is writable and ineffective

The Drive API accepts comment creation via `POST files/{fileId}/comments`, with `content` and
`quotedFileContent` writable, and it exposes an `anchor` field. Inspection of the schema confirms
the field can be set.

Google's own guidance on anchoring, however, states that anchors "are immutable, and their position
relative to the content of a document cannot be guaranteed across revisions", and — decisively —
that Workspace editor applications "treat developer-defined anchored comments **as unanchored
comments** in their display".

The consequence is precise and easy to miss: a program can set the anchor, receive a success
response, and produce a comment that the student sees floating unattached. Verification by API
response is therefore insufficient. The documentation recommends anchoring only where position does
not move — images, read-only documents. A draft the student is still editing is the opposite case.

### 2.2 There is no comment-only scope

The restricted scope `drive.file` covers only files the application itself created or that the user
explicitly opened with it. A student's draft, shared with the instructor by link, is neither.
Commenting on it therefore requires the broad `https://www.googleapis.com/auth/drive` scope.

That scope grants read and write access to **the instructor's entire Drive**, not to the one document
being commented. For an institutional account, that includes every other student's work, every
administrative document and every personal file stored there. The asymmetry is stark: the task needs
write access to a comment thread on one file; the only available key opens everything.

This is a privacy-by-design failure in the platform, not in the tool built on it, and it is worth
naming as such because the usual mitigation — "we only use it for comments" — is a promise, not a
control.

### 2.3 Suggestion mode is absent

Instructors frequently want to propose a wording change rather than comment on it, using the
editor's "Suggesting" mode. A review of the Docs API surface found **no endpoint that creates
suggestions**: of the forty request types available, zero produce a suggested edit. The feature
exists in the interface and not in the API.

## 3. THE WORKAROUND

### 3.1 Using the session the instructor already has

Rather than requesting a broad OAuth grant, the tool drives a real browser instance under the
instructor's existing, ordinary login. The authorisation used is the one already granted when the
student shared the document; no new scope is requested, and no long-lived token with Drive-wide
powers is created or stored.

The anchoring is achieved by the same sequence a human uses: locate the phrase with the editor's own
find function, select it, invoke the comment command, type, and confirm. Because the editor itself
performs the anchoring, the resulting comment is a native anchored comment rather than a
developer-defined one, and is displayed as attached.

This has a cost worth stating: the approach depends on the editor's interface, which can change
without notice, and it cannot run unattended on a server.

### 3.2 Three constraints the find-based approach imposes

Anchoring through the editor's find function is only reliable if the quoted phrase (i) lies within a
single paragraph, (ii) is unique in the document, and (iii) matches **literally**, without
normalisation of spacing or quotation marks. These are not implementation details; they are the
contract, and violating any of them silently places the comment somewhere else or nowhere.

One consequence found in practice: a phrase that also appears in an automatically generated table of
contents is not unique, even though a reader would consider it to occur once. The validation step
must therefore see the document as the find function sees it, including generated content that a
document-parsing library would skip.

### 3.3 Verification by export, not by screen

Every published comment is verified by exporting the document in a format that serialises comments
and their ranges, and confirming that the number of comment records equals the number of
`w:commentRangeStart` markers and the number of `w:commentRangeEnd` markers. An anchored comment
produces all three; an unanchored one produces the record without the range markers.

This check exists because the screen is not evidence. During development we encountered a distinct
but instructive case in a different system: an interface that reported a save as successful while
the underlying record remained empty. Reading the serialised artefact is the only verification that
does not depend on the application agreeing with itself.

## 4. OPERATIONAL SAFEGUARDS, AND AN INCIDENT

The tool publishes to documents belonging to students. That asymmetry — the operator bears none of
the cost of an error, the student bears all of it — justifies safeguards that would be excessive
elsewhere.

**Ordered modes.** Three modes are exposed, in a fixed order: validate the plan against the live
document without writing; publish to a private copy so the instructor reads what the student would
receive; and only then publish to the student's document, behind an explicit confirmation flag.

**Receipts.** Each publication writes a machine-readable record of exactly what was posted, because
a comment carries no marker identifying its author as a program, and without a receipt there is no
principled way to remove one's own comments and not someone else's.

**An incident, reported because it is the evidence.** During operation, eleven comments were
published to a real student document before the instructor had authorised that specific step. The
receipt made complete withdrawal possible, and the withdrawal was verified by export showing zero
remaining comments. The incident is reported here rather than omitted because it demonstrates both
the necessity of the receipt mechanism and the insufficiency of good intentions: the safeguard that
mattered was the one that had been built beforehand.

**A second, subtler finding.** A document may already contain comments that are not feedback at all.
The institutional template used for undergraduate degree projects ships with roughly forty
instruction comments authored under a generic name, which students frequently do not delete. A tool
that does not distinguish these will either duplicate advice already present or misread a template
as a colleague's review.

## 5. DISCUSSION

### 5.1 What this does and does not solve

It solves anchoring, and it solves it without requiring a Drive-wide authorisation. It does not
solve suggestion mode, which remains unavailable by any programmatic route. It does not remove the
instructor from the loop, and by design it should not: the safeguards assume a human authorises each
publication.

It also does not make the feedback good. Nothing in the mechanism improves what is said; it only
ensures that what is said arrives attached to what it is about.

### 5.2 A note on platform dependence

An approach that drives an interface is more fragile than one that calls an API. We accept that
trade-off here because the alternative is not a robust API but a broad authorisation grant with a
cosmetic anchor. When a comment-only scope with functional anchoring becomes available, the correct
move is to abandon this approach entirely.

### 5.3 Threats to validity

The author designed, operated and reports the system, without independent audit. The API findings
were established against the documentation and schema available during one term and could change.
No measurement of feedback quality, student response or instructor time was made.

## 6. CONCLUSIONS

Three things worth knowing before attempting programmatic feedback in Google Docs: the `anchor`
field is writable but rendered as unanchored; commenting on a third party's document requires
Drive-wide access because no narrower scope exists; and suggestion mode has no API. A workaround
built on the instructor's existing session avoids the authorisation problem and produces genuinely
anchored comments, at the cost of interface dependence and the requirement that a human remain in
the loop.

Future work worth doing: a study of whether anchored feedback is acted upon more often than
equivalent unanchored feedback; and a systematic review of comment-anchoring support across the
document platforms used in higher education, since the limitation reported here may not be unique to
one vendor.

## ACKNOWLEDGEMENTS AND DECLARATIONS

**Funding.** Internal research call CUN 2026 — Thematic Research Groups, Phase II. No external
funding.

**Author contributions.** Conceptualisation, methodology, software, original draft, review and
editing: the single signing author.

**Conflict of interest.** The author declares no conflict of interest.

### Data Availability Statement

**Data Availability Statement / Declaración de disponibilidad de datos / Declaração de
disponibilidade de dados.** No research dataset was generated by this work. The findings reported in
Section 2 are statements about a public API and its published documentation, verifiable by any
reader against that documentation. The tool described operates on student documents and its
operational records therefore cannot be shared. Section 3 describes the method in sufficient detail
to reimplement it.

### Declaration on the use of Artificial Intelligence

**Declaration on the use of Artificial Intelligence / Declaración de uso de Inteligencia Artificial.**
Generative artificial intelligence assistants — Claude (Anthropic) and ChatGPT (OpenAI) — were used
in preparing this manuscript for drafting and editing prose and for checking internal consistency,
and were used in building the tool described. No tool generated data, measurements or bibliographic
references that were not individually verified by the author. The author accepts full responsibility
for the content.

**Personal data and ethics.** This manuscript contains no personally identifying information about
any student, and reproduces no student work, identifier or feedback text. The work describes a tool
operated by the author in his own teaching and did not involve research with human subjects; no data
were collected from students and no intervention was applied to them.

---

## REFERENCES

*Note on digital identifiers: entries are presented as verified with respect to authorship, year,
title and source. DOIs and URLs will be incorporated after individual verification in Crossref. No
DOI is transcribed that has not been verified.*

Bennett, R. E. (2011). Formative assessment: A critical review. *Assessment in Education: Principles,
Policy & Practice*, 18(1), 5–25.

Black, P., & Wiliam, D. (1998). Assessment and classroom learning. *Assessment in Education:
Principles, Policy & Practice*, 5(1), 7–74.

Boud, D., & Molloy, E. (2013). Rethinking models of feedback for learning: The challenge of design.
*Assessment & Evaluation in Higher Education*, 38(6), 698–712.

Carless, D., & Boud, D. (2018). The development of student feedback literacy: Enabling uptake of
feedback. *Assessment & Evaluation in Higher Education*, 43(8), 1315–1325.

Cavusoglu, H., Phan, T. Q., Cavusoglu, H., & Airoldi, E. M. (2016). Assessing the impact of granular
privacy controls on content sharing and disclosure on Facebook. *Information Systems Research*,
27(4), 848–879.

Cranor, L. F. (2008). A framework for reasoning about the human in the loop. *Proceedings of the 1st
Conference on Usability, Psychology and Security*.

Ericsson, K. A., Krampe, R. T., & Tesch-Römer, C. (1993). The role of deliberate practice in the
acquisition of expert performance. *Psychological Review*, 100(3), 363–406.

Felt, A. P., Chin, E., Hanna, S., Song, D., & Wagner, D. (2011). Android permissions demystified.
*Proceedings of the 18th ACM Conference on Computer and Communications Security*, 627–638.

Hattie, J., & Timperley, H. (2007). The power of feedback. *Review of Educational Research*, 77(1),
81–112.

Nicol, D. J., & Macfarlane-Dick, D. (2006). Formative assessment and self-regulated learning: A model
and seven principles of good feedback practice. *Studies in Higher Education*, 31(2), 199–218.

Norman, D. A. (2013). *The Design of Everyday Things* (revised ed.). Basic Books.

Reason, J. (1990). *Human Error*. Cambridge University Press.

Sadler, D. R. (1989). Formative assessment and the design of instructional systems. *Instructional
Science*, 18(2), 119–144.

Shute, V. J. (2008). Focus on formative feedback. *Review of Educational Research*, 78(1), 153–189.

Wang, Y., Leon, P. G., Acquisti, A., Cranor, L. F., Forget, A., & Sadeh, N. (2014). A field trial of
privacy nudges for Facebook. *Proceedings of the SIGCHI Conference on Human Factors in Computing
Systems*, 2367–2376.

Winstone, N. E., Nash, R. A., Parker, M., & Rowntree, J. (2017). Supporting learners' agentic
engagement with feedback. *Educational Psychologist*, 52(1), 17–37.
