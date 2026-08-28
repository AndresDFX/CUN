# An Ungraded Survey Gating a 32.8% Assignment in Seven Moodle Courses

**Una encuesta sin nota bloquea una entrega del 32,8 % en Moodle**

---

**Corresponding author**

Julian Andrés Castaño Espinosa
School of Engineering, Corporación Unificada Nacional de Educación Superior — CUN
Bogotá, Colombia
julian_castanoe@cun.edu.co
ORCID: https://orcid.org/0009-0003-6598-432X

**Authorship.** Single author, who designed and operated the audit, wrote the client used to perform
it, applied the corrections and verified them.

**Institutional affiliation of the work:** School of Engineering, CUN.

---

## ABSTRACT

Institutional courses arrive populated by a template, and the instructor corrects what the template
got wrong. This report documents an instrumented audit of seven Moodle 4.5 course instances, and
what the instrument itself could not see. The graded catalogue was clean: 53 graded items aligned to
the departmental schedule, zero discrepancies. The defect lay entirely outside it. The 28
institutional feedback surveys, ungraded and therefore absent from both the schedule table and the
client's activity-type map, kept their template dates: 13 opened in 2028 or 2030 in a course running
in 2026, and 11 of those stored an opening instant identical to their closing instant, a window that
can never open. Such a window passes upstream validation, which rejects only a close strictly
earlier than the open. The consequential finding is a coupling. In two instances the final
assignment, weighted 32.8% with no grace period, was restricted by completion of one of those
surveys, so the survey's opening date became the assignment's effective one, leaving 2 usable days
of 31 in one instance and 10 of 39 in the other, while the calendar displayed the full window. The
correction removed the survey windows, not the institutional restriction; re-reading the server
confirmed that existing responses, stored close dates and every other field were untouched. The
generalisable rule: grade weight predicts neither schedule risk nor blocking power, so a date audit
must enumerate every activity type and resolve every access restriction before declaring a course
correct. No student-level data are reported.

**Keywords:** learning management system; Moodle; conditional release; activity completion;
configuration error

## RESUMEN

El aula institucional llega poblada por una plantilla y el docente corrige lo que quedó mal. Este
informe documenta una auditoría instrumentada de siete aulas Moodle 4.5 y lo que la instrumentación
no vio. El catálogo calificable estaba en orden: 53 ítems alineados con el calendario del programa,
cero discrepancias. El defecto vivía fuera de él. Las 28 encuestas institucionales feedback, sin
nota y por eso invisibles para el instrumento, conservaban sus fechas de plantilla: 13 abrían en
2028 o 2030 en un curso de 2026, y 11 de ellas guardaban una apertura idéntica al cierre, una
ventana que nunca abre. El formulario la acepta: solo rechaza un cierre estrictamente anterior a la
apertura. El hallazgo con consecuencias es un acoplamiento: en dos aulas la entrega final, 32,8 % de
la nota y sin prórroga, estaba restringida por la finalización de una de esas encuestas, así que la
fecha de la encuesta era su apertura real: 2 días útiles de 31 en un aula y 10 de 39 en la otra,
mientras el calendario mostraba la ventana completa. La corrección quitó la ventana de las
encuestas, no la restricción institucional; al releer el servidor, las respuestas y los demás campos
seguían intactos. La regla generalizable: el peso de un ítem no predice su riesgo de calendario ni
su poder de bloqueo; toda auditoría de fechas debe enumerar cada tipo de actividad y resolver cada
restricción de acceso antes de declarar correcta un aula. No se reportan datos de estudiantes.

**Palabras clave:** entorno virtual de aprendizaje; Moodle; acceso condicional; finalización de
actividad; error de configuración

---

## 1. INTRODUCTION

Deployed software is rarely software that was configured from scratch. A running instance is
instantiated from a template, an image or an earlier instance, and whoever inherits it corrects what
does not apply. Configuration errors introduced this way are a documented failure class in
production systems: they have been studied empirically across commercial and open-source software
[1], surveyed as an engineering problem in their own right [2], and shown to grow harder with the
number of independently settable options a system exposes [3]. Their characteristic property is that
no individual setting is wrong. Each value is legal, each subsystem behaves as specified, and the
failure exists only in the composition.

This report is an audit of one such deployed system, and — in equal measure — an audit of the
instrument built to audit it. The system is an institutional deployment of Moodle 4.5, the
open-source platform introduced by Dougiamas and Taylor [4], whose unit of deployment is the
course: a container of activities, resources and the constraints between them. Two of its
subsystems are relevant here, and they are deliberately separate. One schedules activities, storing
per-activity opening, closing, due and cut-off instants. The other, conditional availability,
stores what must be done before an activity becomes reachable [5]. They answer
different questions and are correctly modelled apart. The audit reported below concerns what
happens when they are composed: when the prerequisite named by an availability condition is itself a
schedulable object, the pair yields an effective schedule that neither subsystem stores and neither
interface displays.

The case against which the audit was exercised is seven course instances of that deployment, all
instantiated from institutional templates, taught by the author in the 2026-2 term at a private
Colombian higher-education institution. The instances are the validation case, not the subject: what
is being examined is the configuration state of a deployed system, the tooling used to inspect and
repair it, and the evidence that the repair was confined to what it was meant to touch.

The audit rests on three sources of evidence and one constraint. The sources are the deployment's
own teacher-facing forms, read and written by an authenticated HTTP client written for this work; a
second, independent reader that parses the gradebook pages and recovers weights, scales and
aggregation methods; and the upstream source code of the branch matching the deployed version,
consulted instead of the documentation whenever the question was what the platform actually accepts.
The constraint is that the client holds no capability beyond the teacher role. It drives
`/course/modedit.php`, not a privileged interface, and every write follows a fixed protocol: a null
round-trip before any real change, a minimal field diff, confirmation taken from a fresh read of the
server rather than from the response to the write, and an explicit guard on state the form cannot
edit. That protocol is what allows the results below to be stated as measurements. The role
restriction is deliberate: an audit that requires administrative access is not an audit that the
people who operate a course can run, and Section 3.6 records precisely where that boundary stopped
the repair.

The audit's principal finding is that the instrument was well aimed and blind: it enumerated the
assessed catalogue, found it consistent, and never reached the activities where the whole of the
defect lived, because those activities carry no grade. One of them held the effective opening date
of the largest graded item in its course.

The contributions of this report are the following.

1. **An audit protocol for a template-instantiated deployment**, implemented against the ordinary
   web interface, applied to an audit that enumerated 149 active dates across seven instances, and
   accompanied by before/after evidence that each write was confined to the fields intended.
2. **A source-level account of an accepted degenerate state.** The deployed version's form
   validation rejects only a closing instant strictly earlier than the opening instant, so a window
   whose close equals its open is a legal submission and a permanently unavailable activity [6].
3. **A measured coupling between the availability and scheduling subsystems**, in which an ungraded
   activity determined the effective opening date of an assignment weighted 32.8% of the course
   grade, while the calendar displayed the assignment's full window.
4. **A defect found in the audit instrument itself, and its correction.** The enumeration was driven
   by the assessment schedule, which is exactly the criterion that excludes the offending activities;
   and the safety rule protecting live institutional data was located in the component that decides
   rather than in the component that writes, which is not where a safety rule survives a second
   caller.
5. **An ordering constraint on date-classification rules.** A degenerate window must be tested for
   before "already past", or a rule set silently loses the defect at the moment it becomes permanent.
6. **A divergence between the deployed forms and the upstream source of the version the deployment
   identifies**, established by measurement across all instances of the activity type and reported
   as an open defect that no instructor-level tool can close.

We report what was measured, what was corrected, what could not be corrected at instructor level,
and what the episode implies for anyone auditing a template-instantiated deployment. We claim no
effect on student learning, report no student-level data, and make no counterfactual estimate of how
many submissions the defect prevented — that number was not measured and is not inferable from the
records available.

Section 2 describes the deployment, the two instruments and the write protocol; Section 3 reports
the measurements, the source-code verification and the coupling; Section 4 the correction, the
safeguards it forced into the client, and the evidence that nothing else moved; Section 5 the
causes, the resulting audit rule and the limits of the work.

## 2. SETTING AND INSTRUMENTATION

### 2.1 The seven course instances

The audit covers the seven course instances taught by the author in the 2026-2 term at a private
Colombian higher-education institution, on an institutional Moodle deployment identified internally
as the institutional Moodle and recorded in the maintenance client as Moodle 4.5 — the open-source platform
introduced by Dougiamas and Taylor [4], whose unit of organisation is the course as a container of
activities, resources and the restrictions between them. The seven instances correspond to
five distinct subjects — one subject contributes three parallel groups — and to two levels,
undergraduate engineering and a specialisation programme. Aggregate enrolment across the seven
instances at the time of the gradebook reading was 279 students. No student-level attribute of any
kind was read, stored or reported in this work; the identifiers that appear below are Moodle course
ids and course-module ids (`cmid`), which name platform objects, not people.

All seven instances were created from institutional templates. The template supplies the structure
of the gradebook, the institutional survey activities, a large body of filler content, and the
access restrictions between them.

### 2.2 The client and the verification protocol

Maintenance was performed with an authenticated HTTP client written for this purpose, which drives
the ordinary teacher-facing web forms rather than a privileged interface: it reads
`/course/modedit.php?update=<cmid>`, extracts every form field in document order, changes only the
fields it intends to change, and posts the form back. The client holds no capability that the
teacher role does not have, which matters for the interpretation of Section 3.6.

Every write follows the same protocol, and the protocol is the reason the findings below can be
stated as measurements rather than impressions:

1. **Null round-trip before writing.** The unmodified form is posted back and the result compared,
   so that any field the client mangles is discovered before a real change is attempted.
2. **Minimal diff.** Only the fields corresponding to the requested change are altered; the complete
   before/after field list is compared and reported.
3. **Re-read from the server after writing.** Confirmation is taken from a fresh GET of the form and
   of the student-facing view, never from the response to the POST.
4. **Guard on collateral state.** For the surveys, the stored close date shown in the activity view —
   a value the form cannot edit, see Section 3.6 — is read before and after every write and reported
   if it changes.

Two independent instruments were used, and their agreement is part of the evidence. The maintenance
client reads activity forms. A separate gradebook reader parses `/grade/edit/tree/index.php` and
`/grade/report/grader/index.php` to recover effective weights, scales, aggregation methods and
per-item counts of graded submissions. The 32.8% weight quoted throughout was read by the second
instrument, not asserted by the first.

### 2.3 What counts as measured here

Every figure in Section 3 comes from one of three sources: a form read from the deployment, a
gradebook page read from the deployment, or the upstream Moodle source code retrieved from the
project's public repository on the branch matching the deployed version. Where a quantity was not
measured, this report says so and does not estimate it. In particular, no claim is made about the
number of students who attempted a submission and were blocked, about grade impact, or about the
frequency of this configuration in other institutions.


> **A note on identifiers.** Course instances are named by subject; the two that recur across several sections also carry a short label (Instance A, Instance B), used consistently wherever they appear. The numeric identifiers in the tables are Moodle course ids and course-module ids (`cmid`): they name platform objects, not people, they carry no meaning outside this deployment, and they are retained so that the institution's own administrators can reproduce every reading (see the Data Availability Statement).

## 3. RESULTS

### 3.1 The graded catalogue was consistent

The first pass adjusted every graded item in the seven instances against the departmental schedule
held in the repository. The result was clean, and this is the baseline against which the rest of the
report should be read.

| Metric | Value |
|---|---|
| Course instances | 7 |
| Graded items adjusted | 53 |
| Quizzes | 38 |
| Assignments | 8 |
| Graded forums | 7 |
| Items with a discrepancy after adjustment | 0 |
| Items skipped | 0 |

The gradebook reader independently confirmed, for each instance, that every catalogue item held in
the repository was present in the gradebook, that effective weights matched the repository and summed
to 100.0%, that every grade category aggregated as a weighted mean, and that the graded items shared
a single 0.00–5.00 scale. In one instance it also confirmed that no gradebook item lay outside the
catalogue; in the other six it did not, and what it found there instead is reported in Section 3.7.
Under any audit organised around assessment weight, the seven courses were correct.

### 3.2 The 28 ungraded surveys were never inspected

They were not correct. Each instance carries institutional `feedback` activities — three teaching
evaluations and one learning-environment survey — 28 in total across the seven instances. None of
them was touched by the first pass, for two compounding reasons that are worth separating because
they generalise differently.

The first reason is that the date command never walks the course: it walks the schedule. For each
item in the repository's schedule table it looks up an activity of the same name inside the course
and writes that activity's dates. The schedule table is indexed by assessment item, because it is the
assessment schedule, and ungraded activities are not in it — so the 28 surveys were never candidates
for the writer, and the command's closing summary, which counts the items it was handed, reported
nothing about them. What the tool does not enumerate, the tool cannot fix, and — worse — the tool's
clean report says nothing about it.

The second reason would have blocked the fix even if the first had not. The client's date-field map
associated a set of form field names with each activity type, and it covered three: `quiz`
(`timeopen`, `timeclose`), `assign` (`allowsubmissionsfromdate`, `duedate`, `cutoffdate`,
`gradingduedate`) and `forum` (`duedate`, `cutoffdate`). The type `feedback` was absent, so a survey
that did reach the writer would have been declined for want of a field map; and even with `feedback`
added, the command would still have had no date to write for it. The correction therefore required a
separate sub-command with its own policy, not a new branch of the existing one.

### 3.3 Thirteen surveys that could not open

A census of all 28 surveys, reading `timeopen` from each activity's edit form and the displayed
window from each activity's view page, found 13 with a stored opening date in the template years
2028 and 2030 — in a course term running from August to November 2026.

| Course instance | Surveys with template opening | Stored opening values |
|---|---|---|
| Creatividad y Pensamiento Innovador (Instance B) | 4 | 27 Oct 2030 |
| Investigación en Ciencia y Tecnología (Instance A) | 4 | 18 Feb 2028 |
| Trabajo de Grado 2 (129268) | 1 | 18 Feb 2028 |
| Trabajo de Grado 3, group 54450 (112321) | 1 | 18 Feb 2028 |
| Trabajo de Grado 3, group 54466 (116387) | 1 | 18 Feb 2028 |
| Trabajo de Grado 3, group 54467 (129270) | 1 | 18 Feb 2028 |
| Proyecto I, specialisation (130378) | 1 | 18 Feb 2028 |
| **Total** | **13** | |

Of the 13, **11 stored an opening instant identical to the closing instant**, to the minute: three at
27 Oct 2030 05:31, one at 27 Oct 2030 05:35, five at 18 Feb 2028 11:04 and two at 18 Feb 2028 11:05.
That is a window of zero duration — an activity that opens and closes at the same instant and is
therefore never available. The remaining 2 had a future opening and no stored close at all.

The other 15 surveys had the opening checkbox disabled altogether. They displayed no window, were
permanently available, and contained 206 real student responses. They were functioning precisely
because they had no dates.

The symptom that started the investigation was a student report: an attempt to answer the
learning-environment survey returned a generic error message. The teaching-evaluation activity of one
instance displayed, to the instructor, an opening and a closing at the same minute in February 2028.

### 3.4 Why a zero-duration window is legal

A window whose close equals its open looks like something a form should reject. It is not rejected,
and the reason is visible in the upstream source of the version deployed here. In
`mod/feedback/mod_form.php` on branch `MOODLE_405_STABLE`, the validation method contains a single
date consistency check, which raises an error only when the close is *strictly earlier* than the
open [6]. Equality passes. A template that stamps the same timestamp into both
fields — which is what the observed values look like, since each pair carries one and the same
timestamp and those timestamps take only four distinct values across the seven instances — produces a
valid form submission and a permanently unavailable activity.

This is the pattern Xu et al. [7] describe when they argue that a setting the system accepts but
cannot honour is a defect of the checking code rather than of the person who entered it: the domain
constraint — a window must have positive duration — exists, but the form enforces only its strict
form.

This has an operational consequence for anyone writing an audit rule, and it is the reason the
classification order in Section 4.3 matters: a zero-duration window in the *past* is
indistinguishable, to a naive check, from an activity that opened normally and is now simply
available. The naive rule "flag activities whose opening lies in the future" would have reported
these 13 today and reported nothing at all from 19 February 2028 onwards, at which point they would
be permanently broken and permanently invisible to the audit.

### 3.5 The coupling: an ungraded survey gating a 32.8% assignment

The first corrective pass gave the 13 broken surveys ordinary 2026 opening dates aligned to the
grading periods. Re-reading the courses after that pass surfaced the finding that changed the
decision, and that is the substantive contribution of this report.

In two of the seven instances, the final assignment carries an access restriction of type
*completion* pointing at the third teaching-evaluation survey: literally
`{"type":"completion","cm":<cmid of the survey>,"e":1}` in the module's stored availability
conditions, with the module reporting `hascmrestrictions`. The survey, in turn, is configured to
count as complete only when it is *answered* (`completionview` together with `completionsubmit`), and
it cannot be answered before it opens.

The consequence is a silent transfer of scheduling authority. The assignment's own dates were
correct. Its effective opening date was the survey's opening date.

| Course instance | Final assignment | Its own window | Gating survey | Usable days before | Usable days after |
|---|---|---|---|---|---|
| Investigación (Instance A) | cmid 6522210 | opens 13 Aug, cut-off 12 Sep 23:59 | cmid 6522208, opened 11 Sep | **2 of 31** | 31 of 31 |
| Creatividad (Instance B) | cmid 6745731 | opens 12 Aug, cut-off 19 Sep 23:59 | cmid 6745729, opened 10 Sep | **10 of 39** | 39 of 39 |

Usable days are counted inclusively between the effective unlock and the cut-off. Two aggravating
properties of these assignments matter. First, the weight: the gradebook reader records the final
assignment at **32.8%** of the course grade in both instances — the largest single item in the
undergraduate scheme, ahead of the first partial examination at 24.0%. Second, the absence of any
grace period: the cut-off date equals the due date, so the platform accepts nothing after the
deadline, late or otherwise. A student who discovered the assignment on the last available day had no
recourse inside the platform.

Nothing in the student's view announces the coupling as a scheduling fact. The calendar shows the
assignment's window. The restriction is displayed as a condition to satisfy, not as a date, and the
condition is on an activity that carries no grade and is presented as an institutional formality.

### 3.6 A field the deployment's form does not expose

Correcting the openings was possible. Correcting the closes was not, and the reason is a difference
between the deployed forms and the upstream code.

Measured across all 28 surveys: in `/course/modedit.php?update=<cmid>` for a `feedback` activity in
this deployment, the only date selectors present are `timeopen` and `completionexpected`. The string
`timeclose` does not occur anywhere in the served HTML — not as a field, not as a label. The
fieldset legends read "Availability" and "Allow answers from". The close date that the student-facing
view does display comes from the stored record and cannot be reached through the form.

The upstream source for the same version does define that field: `mod/feedback/mod_form.php` on
`MOODLE_405_STABLE` adds a `date_time_selector` for `timeclose` immediately after the one for
`timeopen` [6]. The deployed form therefore diverges from the upstream form of
the version the client identifies. This report does not establish the cause of the divergence — a
local customisation, a plugin, a role-level form restriction and a version mismatch are all
consistent with what was observed, and distinguishing them requires access this author does not have.
What is established is the operational consequence, and it is not small: **11 stored close dates
remain in 2028 and 2030**, and they are the only dates in the seven instances that are not 2026
dates. The audit counted 149 active dates in all — 135 on activity forms and 14 at course level — so
138 of them are 2026 dates and 11 are not. Those 11 belong to institutional teaching-evaluation
surveys, which will therefore keep accepting responses between roughly seventeen months and four
years after their courses close grades. Two further surveys have no stored close at all and remain
open indefinitely; they were not emptied of a close date, they never had one.

Course-level dates are equally out of reach: they arrive frozen for the teacher role, and only an
administrator can move them.

### 3.7 The same blind spot on a second axis

The pattern found in the date audit — that the graded catalogue is well tended and everything outside
it is not — was independently visible in a different maintenance task performed on the same courses,
and the agreement is worth recording because it suggests the blind spot is structural rather than
incidental.

A visibility pass classified every course component by whether it carries weight in the gradebook,
reading the weight from the gradebook tree rather than inferring it from the component's name. Across
the seven instances the pass left **168 components visible and hid 101, with 0 errors**, every action
reversible by a single command. All but one of the hidden components were template filler: SCORM
packages and pages named "Contenido N (haz clic aquí)", placeholder links named "G1 … G8",
"Video 1 … Video 8" and "Recurso 1 … Recurso 8" — one set per topic — interactive-image and podcast
pages, an institutional "Modelo pedagógico" page in every instance, and empty text-and-media areas.
The single exception was a test forum the author had created himself. The instance with the largest
amount of filler contributed 35 hidden components; three instances contributed 2 each.

The case that prompted that pass is a useful miniature of the whole problem. A pair of template
forums, visible to students, had an empty description and a single existing discussion whose opening
post had an empty body, stamped by the template. Both were of the "single simple discussion" type, in
which a student cannot open a new thread and can only reply to the existing — blank — message.
Neither had a gradebook item at all and neither was rated, so neither could produce a grade. The same
pair was then found, also empty and also visible, in a second instance. Students asked what they were
supposed to do there, which is the only reason anyone looked.

The gradebook reader, working from a different page, corroborated the same phenomenon from the other
direction: it counted **18 template filler items that do have a gradebook entry but carry 0% weight**,
distributed across six of the seven instances (8, 1, 1, 1, 1 and 6), on 0.00–1.00 and 0.00–100.00
scales, and verified that they move no grade. Two instruments, two pages, one conclusion: in a
template-populated course, the set of components that matter and the set of components that look
official are different sets, and the difference is not legible from a component's name.

## 4. THE CORRECTION AND ITS SAFEGUARDS

### 4.1 What was changed, and what deliberately was not

The corrective decision reversed the first pass. Rather than schedule the teaching-evaluation surveys
sensibly, all six that carried windows were left with **no opening date at all** — the configuration
that the other 15 surveys already had, and the configuration under which they work. Six writes, each
verified by re-reading the server. The learning-environment survey in all seven instances received a
single opening date, 10 August 2026, the term start date recorded for the five subjects; it is in the
past, so the activity is available now, and it is the only survey date the repository actually
declares.

Two things were deliberately not changed. The access restriction on the final assignment was left
exactly as the template placed it, still pointing at the survey's completion, verified unchanged by
re-reading the server: it is an institutional requirement that students evaluate their teaching, and
removing it would silently remove that requirement. Once the survey is always available, the lock can
be opened on any day of the assignment's window, so the restriction stops being a scheduling
constraint and becomes what it was meant to be — a task ordering. The 15 already-working surveys were
not touched either, for the reason given in Section 4.2.

The other access restrictions in these two instances were checked and were consistent: the first quiz
and first partial with the first evaluation, the second pair with the second, the third quiz with the
third, and the self- and peer-assessment activities with the learning-environment survey, which opens
at term start.

### 4.2 The guard belongs on the writing path

The 15 functioning surveys had their opening checkbox disabled and contained 206 student responses.
Giving one of them a window would have closed a live institutional data collection. The census
sub-command already refused to touch them, but the census is the component that *decides*; the
component that *writes* is a generic date setter shared with quizzes and assignments, and it emits an
enabled flag for every date field it sets. Adding `feedback` to the type map therefore re-opened, at
the level of the shared writer, exactly the risk the census had closed at the level of the policy.

The guard was moved to the writer: if a survey arrives with its opening disabled, the writer does not
enable it and says so. The regression check is a dry-run plan over the two instances involved in the
incident, which still proposes the same 8 graded items each, zero surveys, zero problems.

The general form of this lesson: a safety rule enforced in the component that chooses actions is not
enforced at all once a second caller reaches the component that performs them.

### 4.3 Ordering the classification rules

The census classifies each survey into one of four states, and the order in which the tests are
applied is load-bearing:

| State of the opening | Verdict |
|---|---|
| Disabled | Working, do not touch — never enable a disabled window |
| Enabled, and open equals close | Zero-duration window: broken, correct it |
| Enabled and already past | Already opened, do not touch |
| Enabled and still in the future | Never opens: broken, correct it |

The zero-duration test is evaluated *before* the already-past test. With only the other three rules,
the defect that motivated all of this work — open equals close equals 18 February 2028 11:04 — would
have been reported as broken until that date and then reclassified as "already opened, do not touch"
from 19 February 2028 onwards, while remaining permanently closed. A rule set can lose a defect by
the passage of time.

A template date stored in 2028 is a latent configuration error in the sense of Xu et al. [8]: it is
accepted when written and becomes damaging only when a separate mechanism — here the completion
restriction — evaluates it, which is why the check must run at census time rather than at
manifestation time.

A companion correction was required in the parser that reads the displayed window: Moodle writes past
labels in a different grammatical form than future ones, and the parser recognised only the future
form. This mattered twice over. It made every survey corrected to a past date print an empty window,
indistinguishable from having lost its opening; and, more seriously, it would have blinded the only
guard watching a field the form cannot edit, since a stored close moving into the past would be
labelled in the past form and read as absent both before and after a write.

### 4.4 Evidence that nothing else moved

The final census re-read all 28 surveys from the server after both passes.

| Check | Result |
|---|---|
| Surveys with an opening in 2028 or 2030 | 0 (were 13) |
| Surveys with a zero-duration window | 0 (were 11) |
| Permanently available, no window | 21 (the 15 that already worked, plus the 6 rectified) |
| Learning-environment surveys with an opening | 7, at 10 Aug 2026 00:00, already open |
| Student responses in the untouched group | 206 of 206, counted survey by survey |
| Untouched surveys that acquired a window | 0 |
| Surveys left hidden by the operation | 0 of 28 |
| Writes that moved a stored close date | 0 of 19 |
| Final-assignment restriction still in place | Yes, in both instances, and satisfiable from day one |

The strongest single piece of evidence that the writes were surgical is the field-level diff: for each
survey written, the complete before/after comparison of the 62 form fields shows **exactly 5
differences**, the five components of the opening date-time selector, with the enabled flag set both
before and after. Visibility, description, question count, item identifiers and responses are
identical. The stored close dates retain their original template timestamps to the minute — 11:04,
11:05, 05:31, 05:35 — which is itself the proof that no write reached them.

## 5. DISCUSSION

### 5.1 Three compounding causes

The defect reported in Section 3.5 required three independent conditions, none of which is a
programming error in the platform.

**A template carrying dates from another instance.** Template dates in 2028 and 2030 are not
plausible values for any current course; they are residue from whatever instance the template was
captured in. The platform accepts them because there is nothing incoherent about a course scheduled
in 2030, and accepts the zero-duration form of them because the validation rejects only strict
inversion (Section 3.4). A course instantiated from a template is a clone in the sense studied by
Juergens et al. [9], and their result — that inconsistently maintained clones induce faults — is the
mechanism at work here: the 2026 instance diverged from the template in everything the schedule table
enumerated, and stayed identical to it in everything the table did not.

**Maintenance tooling organised by grade weight.** Both the schedule table and the client's type map
enumerate what is assessed. This is a reasonable organising principle — it is the principle under
which the 53 graded items came out correct — and it is precisely the principle that excludes the
activities that turned out to hold the keys. Weight predicts audit coverage; it does not predict
blocking power.

**Restrictions stored separately from schedules.** The platform models "when is this available" and
"what must be done first" as different mechanisms, and correctly so: they answer different questions
[5]. But when the prerequisite is itself schedulable, the composition of the two
mechanisms yields an effective schedule that neither mechanism displays. This is a configuration
composition hazard rather than a fault, of the family documented in production systems generally
[1], [2], aggravated by the sheer number of independently settable options
a modern LMS activity exposes [3], and it has the property those authors emphasise: the
individual settings are each defensible, and the failure exists only in their interaction. That is
the standard anatomy of an accident in a tightly coupled system — a latent condition planted by one
decision and triggered by another, with no single actor in a position to see both [10], [11] — and it
argues, as Leveson [12] does for safety generally, for treating the
constraint between components, rather than each component's own correctness, as the thing to be
enforced. It is also, in the
vocabulary of technical debt, a form of configuration debt that accrues at instantiation time rather
than at development time [13]–[15], and that
the person who inherits the course pays.

### 5.2 A rule practitioners can apply

The audit rule that follows from this episode is short enough to state as a sentence and can be
carried out with the ordinary teacher interface: **before giving an opening date to any activity,
determine which items name it as a completion condition, and confirm that none of them opens
earlier.** Its converse is equally useful: **when an assignment's usable window is shorter than its
displayed window, look for a completion condition pointing at an ungraded activity.**

Stated this way, the rule is a configuration smell in the sense of Sharma et al. [16] — a recurrent,
mechanically detectable pattern in declarative configuration — and the census of Section 4.3 is its
detector, applicable to any Moodle course through the ordinary teacher interface.

Three corollaries earned in this work are worth stating with it. An activity whose window cannot be
edited from the form is a permanent liability, so its state must be watched rather than assumed. A
safety rule must live in the code that writes, not only in the code that decides. And a rule set that
classifies by date must test for degenerate windows before testing for "already past", or it will
lose the defect exactly when it becomes unfixable.

### 5.3 Why the visible calendar is not the effective calendar

The student-facing consequence is the part with pedagogical weight, and it is worth naming precisely,
because it is not a usability nuisance. The platform displayed an assignment window of 31 days and
enforced one of 2. A student planning against the displayed window — which is the only window
available to them — plans against a fiction. The literature on deadlines and self-regulation is built
on the assumption that the stated deadline is the
operative one [17], [18], and the design literature on assessment
assumes that students can see the conditions under which they are assessed [19]–[21]. A hidden gate
breaks that assumption without
announcing itself, and it does so asymmetrically by construction rather than by anything measured
here: it is the student who starts early who meets the block, with no way to tell from the interface
whether it is temporary. The mismatch between displayed state and enforced state is the classic
violation of visibility of system status
[22], [23], here with a consequence measured in grade weight rather than in
frustration.

There is also a compliance cost of the kind Herd and Moynihan [24] call a learning cost: the student
must work out, unaided, that an ungraded formality is the thing standing between them and a
submission. The visibility findings of Section 3.7 raise that cost further, since a course populated
with 101 components that turned out to be filler offers no reliable way to tell an institutional
formality that matters from one that does not.

### 5.4 Threats to validity and limitations

**Single institution, single term, single operator.** All seven instances belong to one deployment,
one academic term and one instructor. The specific numbers are not a sample of anything; they
characterise this deployment. What generalises is the mechanism and the audit rule, not the
prevalence.

**No outcome was measured.** We do not know how many students attempted the blocked assignment, and
we make no claim about grades. The defect was corrected on 17 August 2026, before the first affected
due date, so no final grade in these instances was computed under the blocked configuration. Any
statement about learning impact would be unmeasured, and none is made; the traces an LMS keeps
describe activity on a platform rather than learning, and reading them as the latter is precisely the
inference this report declines to make [25].

**The divergence in Section 3.6 is not explained.** We establish that the deployed form lacks a field
that the upstream source of the identified version defines, and we establish the consequence. We do
not establish why, and we could not: diagnosing it requires administrative access.

**The correction is verified, not proved permanent.** Verification is a re-read of the server at a
point in time. Templates are re-applied at each new term, and nothing in this work prevents the same
dates from arriving again in 2027. What the work leaves behind is the census that will detect them.

**Instrument bias.** Both instruments were written by the author, and a systematic misreading of the
gradebook tree or of the activity form would be invisible to both. The mitigations were independence
of source page and cross-checking of the quantities both instruments can see — the presence of a
graded item and the dates it carries, which the maintenance client writes on the activity form and
the gradebook reader recovers from the gradebook — and these agreed for all 53 items.

## 6. CONCLUSIONS

We audited the configuration of a deployed Moodle 4.5 installation across seven template-instantiated
course instances, using only the capabilities of the teacher role, two independent readers of two
different sets of server pages, and the upstream source of the branch the deployment identifies. The
assessed catalogue came out consistent — 53 graded items, zero discrepancies — and the whole of the
defect lay outside it.

Of 28 ungraded institutional surveys, 13 carried template opening dates in 2028 and 2030, and 11 of
those stored an opening instant identical to their closing instant: a window that never opens. That
state is not rejected by the platform, and the source explains why — the version's form validation
raises an error only when the close is strictly earlier than the open, so equality passes and
produces a valid submission for a permanently unavailable activity.

The consequential finding is the coupling between the two subsystems. In two instances the final
assignment, weighted 32.8% with no grace period, was gated by *completion* of one of those surveys,
so the survey's opening date was the assignment's effective opening date: 2 usable days of 31 in one
instance, 10 of 39 in the other, against a calendar that displayed the full window. Neither
subsystem is at fault on its own, and neither stores or displays the schedule their composition
enforces.

The correction removed the surveys' windows rather than the institutional restriction, and it was
verified by re-reading the server rather than by trusting the writes: 206 existing responses intact,
0 of 19 writes touching a stored close date, and a 62-field before/after form diff showing exactly
the 5 intended changes. One limit could not be passed at instructor level: the deployment's survey
form exposes no close-date field although the upstream source of the identified version defines one,
leaving 11 stored close dates in 2028 and 2030 out of 149 active dates. That is reported here as an
open defect requiring administrative action, not as a solved problem, and the cause of the
divergence is not established.

The audit also returned findings about the audit. The instrument was blind for a principled reason:
it enumerated the assessment schedule, which is exactly the criterion that excludes the activities
that held the keys. The safety rule that protected 206 live responses sat in the component that
chooses actions, and was therefore not enforced once a second caller reached the component that
performs them; it now sits on the writing path. And the classification rules had to be ordered so
that a degenerate window is tested for before "already past", because otherwise the defect would
have been reported as broken until February 2028 and reclassified as benign from the following day,
while remaining permanently closed. The same blind spot was visible on a second axis in the same
instances: a visibility pass left 168 components visible and hid 101 with 0 errors, all but one of
them template filler, and the gradebook reader independently counted 18 filler items that hold an
entry in the gradebook but carry 0% weight — which is why the blind spot reads as structural rather
than incidental.

The generalisable results are a rule and a warning, and both are stated for practitioners who can
apply them with an ordinary account. The rule: before giving an opening date to any activity,
resolve which items name it as a completion condition and confirm that none of them opens earlier;
and when an item's usable window is shorter than its displayed window, look for a completion
condition on something that carries no weight. The warning: in a template-instantiated system,
maintenance tooling organised around what is assessed will produce a clean report about a broken
deployment, because an object's weight predicts neither its schedule risk nor its blocking power. An
audit that intends to declare a course correct must enumerate every activity type and resolve every
access restriction, and it must watch the state it cannot edit.

## ACKNOWLEDGEMENTS AND DECLARATIONS

**Funding.** No funding was received for this work.

**Author contributions.** Conceptualisation, methodology, software, data curation, formal analysis,
original draft, review and editing: the single signing author.

### Conflict of interest

**Conflict of interest / Conflicto de intereses.** The author declares no conflict of interest. The
author is an instructor at the institution whose learning management system deployment is described,
and audited his own courses; he holds no financial or commercial relationship with Moodle Pty Ltd.,
with the deployment's operator, or with any vendor named in this manuscript, and received no payment
or benefit conditioned on the content of this report.

### Data Availability Statement

**Data Availability Statement / Declaración de disponibilidad de datos / Declaração de
disponibilidade de dados.** No research dataset was generated by this work, and no dataset can be
shared. The measurements reported are readings of an authenticated institutional learning management
system that is not publicly accessible and whose pages contain enrolled students' personal data;
publishing exports of those pages would be neither lawful nor possible. What is reported here are
aggregate counts and platform object identifiers (course ids and course-module ids), which are
included in the text so that the institution's own administrators can reproduce every reading. The
two verifiable external sources are cited in full and are public: the upstream Moodle source file and
branch used in Sections 3.4 and 3.6 [6], and the platform's availability documentation [5]. The audit
procedure is described in Section 2.2 in sufficient detail to be reimplemented against any Moodle
deployment by a reader with teacher-level access to their own courses.

### Declaration on the use of Artificial Intelligence

**Declaration on the use of Artificial Intelligence / Declaración de uso de Inteligencia
Artificial.** Generative artificial intelligence assistants — Claude (Anthropic) and ChatGPT (OpenAI)
— were used in the preparation of this manuscript for drafting and editing prose, for translating the
abstract, and for checking internal consistency between the figures reported in the text and the
audit records they come from. They were also used while writing the maintenance client described in
Section 2.2. No assistant generated measurements, and no figure in this manuscript was produced by an
assistant: every quantity was read from the deployment or from the cited source code, and was checked
individually by the author. No bibliographic reference was accepted without individual verification.
The author accepts full responsibility for the content of the manuscript.

### Personal data and ethics

**Personal data and ethics / Datos personales y ética.** This manuscript contains no personally
identifying information about any student: no names, no identity or enrolment numbers, no individual
grades, no submission contents and no survey responses. All student-related quantities reported are
aggregates at the level of a course instance (enrolment counts, response counts, per-item counts of
graded submissions). The identifiers that appear in the text are Moodle course and course-module
identifiers,
which designate platform objects. The work is an administrative audit of the author's own course
configuration, carried out with the ordinary permissions of his teaching role; it involved no
research with human subjects, no intervention applied to students, no collection of data from
students, and no processing of personal data beyond the incidental exposure inherent in a teacher
viewing his own gradebook. For that reason no ethics committee approval was sought, and none is
required under the institution's rules for administrative work of this kind. The single
student-originated observation quoted — an error message received when opening a survey — is reported
without any attribute of the person who reported it.

---

## REFERENCES

*Note on digital identifiers: every entry below was verified individually against an authoritative
record (Crossref, DBLP, OpenAlex, Open Library, or the publisher's own page). A DOI is transcribed
whenever one is registered and was resolved through https://doi.org/ (17 entries); where no DOI
exists, a publisher or repository URL was retrieved and confirmed to resolve (6 entries); two printed
books, [10] and [23], carry neither, and no DOI belonging to a different edition or translation was
attached to them. All resolutions were performed on 25 August 2026.*

[1] Z. Yin, X. Ma, J. Zheng, Y. Zhou, L. N. Bairavasundaram, and S. Pasupathy, "An empirical study on configuration errors in commercial and open source systems," in *Proc. 23rd ACM Symposium on Operating Systems Principles (SOSP '11)*, 2011, pp. 159–172. https://doi.org/10.1145/2043556.2043572

[2] T. Xu and Y. Zhou, "Systems approaches to tackling configuration errors: A survey," *ACM Computing Surveys*, vol. 47, no. 4, art. no. 70, pp. 1–41, 2015. https://doi.org/10.1145/2791577

[3] T. Xu, L. Jin, X. Fan, Y. Zhou, S. Pasupathy, and R. Talwadker, "Hey, you have given me too many knobs! Understanding and dealing with over-designed configuration in system software," in *Proc. 2015 10th Joint Meeting on Foundations of Software Engineering (ESEC/FSE 2015)*, 2015, pp. 307–319. https://doi.org/10.1145/2786805.2786852

[4] M. Dougiamas and P. Taylor, "Moodle: Using learning communities to create an open source course management system," in *Proc. EdMedia: World Conference on Educational Media and Technology 2003*, Association for the Advancement of Computing in Education, 2003, pp. 171–178. [Online]. Available: https://researchrepository.murdoch.edu.au/id/eprint/36645/. [Accessed: Aug. 25, 2026].

[5] Moodle Pty Ltd., "Availability API," Moodle Developer Resources, version 4.5. [Online]. Available: https://moodledev.io/docs/4.5/apis/subsystems/availability. [Accessed: Aug. 25, 2026].

[6] Moodle Pty Ltd., "mod/feedback/mod_form.php," Moodle source code, branch MOODLE_405_STABLE (Moodle 4.5, released Oct. 7, 2024), 2024. [Online]. Available: https://github.com/moodle/moodle/blob/MOODLE_405_STABLE/mod/feedback/mod_form.php. [Accessed: Aug. 25, 2026].

[7] T. Xu, J. Zhang, P. Huang, J. Zheng, T. Sheng, D. Yuan, Y. Zhou, and S. Pasupathy, "Do not blame users for misconfigurations," in *Proc. 24th ACM Symposium on Operating Systems Principles (SOSP '13)*, Farmington, PA, USA, 2013, pp. 244–259. https://doi.org/10.1145/2517349.2522727

[8] T. Xu, X. Jin, P. Huang, Y. Zhou, S. Lu, L. Jin, and S. Pasupathy, "Early detection of configuration errors to reduce failure damage," in *Proc. 12th USENIX Symposium on Operating Systems Design and Implementation (OSDI '16)*, Savannah, GA, USA: USENIX Association, 2016, pp. 619–634. [Online]. Available: https://www.usenix.org/conference/osdi16/technical-sessions/presentation/xu. [Accessed: Aug. 25, 2026].

[9] E. Juergens, F. Deissenboeck, B. Hummel, and S. Wagner, "Do code clones matter?," in *Proc. 2009 IEEE 31st International Conference on Software Engineering (ICSE)*, Vancouver, BC, Canada, 2009, pp. 485–495. https://doi.org/10.1109/ICSE.2009.5070547

[10] C. Perrow, *Normal Accidents: Living with High-Risk Technologies*. New York, NY, USA: Basic Books, 1984.

[11] J. Reason, *Human Error*. Cambridge, U.K.: Cambridge University Press, 1990. https://doi.org/10.1017/CBO9781139062367

[12] N. G. Leveson, *Engineering a Safer World: Systems Thinking Applied to Safety*. Cambridge, MA, USA: MIT Press, 2011. https://doi.org/10.7551/mitpress/8179.001.0001

[13] W. Cunningham, "The WyCash portfolio management system," *ACM SIGPLAN OOPS Messenger*, vol. 4, no. 2, pp. 29–30, 1992. https://doi.org/10.1145/157710.157715

[14] P. Kruchten, R. L. Nord, and I. Ozkaya, "Technical debt: From metaphor to theory and practice," *IEEE Software*, vol. 29, no. 6, pp. 18–21, 2012. https://doi.org/10.1109/MS.2012.167

[15] D. Sculley, G. Holt, D. Golovin, E. Davydov, T. Phillips, D. Ebner, V. Chaudhary, M. Young, J.-F. Crespo, and D. Dennison, "Hidden technical debt in machine learning systems," in *Advances in Neural Information Processing Systems 28 (NIPS 2015)*, Curran Associates, 2015. [Online]. Available: https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html. [Accessed: Aug. 25, 2026].

[16] T. Sharma, M. Fragkoulis, and D. Spinellis, "Does your configuration code smell?," in *Proc. 13th International Conference on Mining Software Repositories (MSR '16)*, Austin, TX, USA, 2016, pp. 189–200. https://doi.org/10.1145/2901739.2901761

[17] D. Ariely and K. Wertenbroch, "Procrastination, deadlines, and performance: Self-control by precommitment," *Psychological Science*, vol. 13, no. 3, pp. 219–224, 2002. https://doi.org/10.1111/1467-9280.00441

[18] P. Steel, "The nature of procrastination: A meta-analytic and theoretical review of quintessential self-regulatory failure," *Psychological Bulletin*, vol. 133, no. 1, pp. 65–94, 2007. https://doi.org/10.1037/0033-2909.133.1.65

[19] G. Gibbs and C. Simpson, "Conditions under which assessment supports students' learning," *Learning and Teaching in Higher Education*, no. 1, pp. 3–31, 2005. [Online]. Available: https://eprints.glos.ac.uk/3609/. [Accessed: Aug. 25, 2026].

[20] D. J. Nicol and D. Macfarlane-Dick, "Formative assessment and self-regulated learning: A model and seven principles of good feedback practice," *Studies in Higher Education*, vol. 31, no. 2, pp. 199–218, 2006. https://doi.org/10.1080/03075070600572090

[21] D. Boud and E. Molloy, "Rethinking models of feedback for learning: The challenge of design," *Assessment & Evaluation in Higher Education*, vol. 38, no. 6, pp. 698–712, 2013. https://doi.org/10.1080/02602938.2012.691462

[22] J. Nielsen, "Enhancing the explanatory power of usability heuristics," in *Proc. SIGCHI Conference on Human Factors in Computing Systems (CHI '94)*, 1994, pp. 152–158. https://doi.org/10.1145/191666.191729

[23] D. A. Norman, *The Design of Everyday Things*, revised and expanded ed. New York, NY, USA: Basic Books, 2013.

[24] P. Herd and D. P. Moynihan, *Administrative Burden: Policymaking by Other Means*. New York, NY, USA: Russell Sage Foundation, 2018. https://doi.org/10.7758/9781610448789

[25] D. Gašević, S. Dawson, and G. Siemens, "Let's not forget: Learning analytics are about learning," *TechTrends*, vol. 59, no. 1, pp. 64–71, 2015. https://doi.org/10.1007/s11528-014-0822-x

---

## OPCIONES DE TITULO DESCARTADAS

El titulo que va puesto arriba es el recomendado por el agente de titulos (EN-1 / ES-1): es el unico
par que lleva el numero, y «32.8%» es lo que convierte el hallazgo en noticia. Las otras opciones
quedan aqui por si el Docente prefiere otra; para cambiarlas basta con mover la linea al encabezado.

**Ingles**

- EN-2 (12 palabras) — opcion «mecanismo primero», mejor para indexacion por el termino tecnico:
  *Completion Gating in Moodle: When an Ungraded Survey Locks a Graded Assignment*
- EN-3 (12 palabras) — la mas generica de las tres:
  *Ungraded Activities Can Gate Graded Work: A Date Audit of Moodle Courses*

**Espanol**

- ES-2 (12 palabras) — mecanismo primero:
  *Restriccion por finalizacion en Moodle: una encuesta sin nota bloquea la entrega*
  (variante con la palabra de la casa, tambien 12: «…una encuesta sin nota canda la entrega»)
- ES-3 (12 palabras) — la mas generica; no dice que quien bloquea es una actividad sin nota:
  *Fechas de plantilla y bloqueos ocultos: auditoria de siete aulas Moodle 4.5*
- Variante espejo del EN-1, si la revista exige que titulo e ingles sean traduccion exacta (12
  palabras, pierde el 32,8 %):
  *Una encuesta sin nota bloquea la entrega final en siete aulas Moodle*

---

## PENDIENTE ANTES DE ENVIAR

Esta seccion NO forma parte del articulo. Se borra antes de subir el manuscrito.

### Produccion editorial

1. **Maquetacion en la plantilla del ITM.** TecnoLogicas exige su propia plantilla de Word. Falta
   volcar este Markdown a ella: las 5 tablas van como tablas de Word con titulo y numeracion
   («Tabla 1» … «Tabla 5»), y el articulo no tiene figuras (0), asi que no hay lista de figuras.
2. **Carta de presentacion (cover letter)** dirigida al editor: novedad del hallazgo, por que encaja
   en el alcance de la revista, declaracion de que no esta en evaluacion en otra parte.
3. **Tres evaluadores propuestos**, con nombre, filiacion, correo institucional y ORCID, sin
   conflicto de interes con el autor ni con la CUN. Perfiles que encajan: (a) ingenieria de software
   / configuracion de sistemas, (b) tecnologia educativa o administracion de LMS, (c) factores
   humanos o usabilidad. AUN NO PROPUESTOS: no se inventan nombres aqui.
4. **Formularios de la revista**: cesion de derechos / licencia CC, declaracion de originalidad y
   declaracion de conflicto de intereses firmadas.

### Decisiones que dejo abiertas cada pieza y que el Docente debe cerrar

5. **Normas reales de TecnoLogicas sin verificar.** El agente de titulos trabajo con el tope de 12
   palabras y el rango de 240-250 del resumen tal como se le dieron, sin consultar la guia publicada.
   Hay que comprobar en la web de la revista: tope de palabras del titulo, rango del resumen, numero
   maximo de palabras clave, y si existe tope de extension del cuerpo.
6. **Extension del cuerpo.** Medido: el cuerpo (secciones 1-6) pasa de 5.531 a 6.612 palabras, es
   decir +1.112 (+20,1 %); la cifra de «935 palabras» que circulo antes no contaba las frases de las
   cuatro referencias nuevas, y la de «6.612» es de antes de reescribir la nota de identificadores. Si
   la revista pone tope duro, los dos primeros recortes son la lista de seis contribuciones (se
   comprime a un parrafo en prosa, ~150 palabras menos) y la frase de hoja de ruta al final de la
   Seccion 1 (~60 palabras menos); ninguno de los dos toca el reencuadre.
7. **Limite de la Seccion 3.6 fuera del abstract.** El resumen condensado ya no menciona que el
   formulario desplegado no expone `timeclose` y que 11 cierres siguen en 2028 y 2030. Si se quiere
   dentro, cabe acortando la frase de apertura y anadiendo: «One limit remains: the deployed form
   exposes no close-date field, so 11 stored closes stay in 2028 and 2030.»
8. **Asimetria menor EN/ES en el resumen.** El ingles dice «passes upstream validation» (atribuye la
   comprobacion al codigo fuente); el espanol dice «El formulario la acepta». Si se quiere simetria
   exacta: «El codigo fuente la acepta: solo rechaza…» (+1 palabra, quedaria en 250).
9. **Referencia [12] (Leveson), ano en disputa: se queda en 2011.** Crossref y OpenAlex fechan la
   edicion con DOI en 2012-01-13, pero Open Library registra una tirada de MIT Press de 2011 (y otra
   de 2012), asi que 2011 esta respaldado por un registro comprobable y no solo por la costumbre de
   cita. Aviso: el motivo que se dio antes para conservarlo («no desalinear el cuerpo») ya no aplica
   —el cuerpo cita en formato IEEE numerico y no lleva ningun ano—, asi que cambiarlo a 2012 tampoco
   rompe nada. Si el corrector lo objeta, se toca solo la entrada [12].
10. **Referencia [15] (Sculley et al.): las paginas SI se pueden reponer.** Se habian quitado porque
    el BibTeX de NeurIPS trae `pages` vacio, pero DBLP registra el trabajo en NIPS 2015 con
    «pages 2503-2511». Si se quiere la entrada completa, anadir «pp. 2503–2511» esta respaldado.
11. **Referencia [8] (OSDI '16) sin DOI: confirmado que no tiene.** DBLP registra el trabajo en OSDI
    2016, pp. 619-634, y tampoco le asigna DOI; el identificador del ACM DL 10.5555/3026877.3026925
    devuelve 404 y por eso NO se transcribe. Si TecnoLogicas exige DOI en todas las referencias, esta
    es la unica que hay que justificar ante edicion (se cita por la URL de USENIX, verificada con
    HTTP 200, igual que su PDF oficial).
12. **Referencias [10] (Perrow 1984) y [23] (Norman 2013) sin DOI, a proposito.** Los DOIs que
    existen pertenecen a otras ediciones (Princeton 1999 y la traduccion alemana de Vahlen 2016);
    pegarlos a estas entradas falsearia el registro. Ambas ediciones estan verificadas en Open
    Library y por resenas contemporaneas.
13. **Concentracion de autoria en las referencias de sistemas.** Con [7] y [8] nuevas, el articulo
    cita cuatro trabajos del grupo Xu/Zhou (contando [2] y [3], que ya estaban). Es defendible —es el
    grupo canonico de misconfiguration—, pero si se prefiere diversificar, hay un repuesto
    verificado: A. Rahman, R. Mahdavi-Hezaveh y L. Williams, «A systematic mapping study of
    infrastructure as code research», *Information and Software Technology*, vol. 108, pp. 65-77,
    2019, https://doi.org/10.1016/j.infsof.2018.12.004 (HTTP 302 comprobado). Sustituiria a [7], a
    costa del argumento mas afilado de la Seccion 3.4.
14. **Ciudades de editorial** en los libros ([10], [11], [12], [23], [24]): son convencion IEEE, pero
    TecnoLogicas a veces las omite. Quitarlas no rompe nada.
15. **Rangos contraidos de citas** (`[13]–[15]`, `[19]–[21]`): convencion IEEE para tres o mas
    consecutivos. Si la revista los quiere expandidos, son `[13], [14], [15]` y `[19], [20], [21]`.
16. **Tema sin literatura de respaldo.** No se encontro literatura revisada por pares sobre
    liberacion condicional / adaptive release en LMS que sostenga una afirmacion concreta de este
    articulo; solo documentacion de producto (ya citada en [5]) y literatura pedagogica de
    aprendizaje adaptativo, que no sostiene la tesis de sistemas. No se anadio nada ahi y no se
    afirma ninguna novedad no comprobada. Lo mismo con plantillas y clonado de cursos en LMS, que
    queda cubierto por analogia con [9].
17. **Version en espanol del cuerpo.** El manuscrito se queda en ingles (TecnoLogicas acepta ambos).
    Solo el titulo, el resumen y las palabras clave van bilingues, como ya estan aqui.
18. **Referencia [24] (Herd y Moynihan), ano a decidir: el manuscrito dice 2018 y los registros dicen
    2019.** Crossref (el registro del propio DOI citado), OpenAlex y Open Library fechan el libro de
    Russell Sage en 2019-01-09; ningun registro alcanzable dice 2018, aunque 2018 es el ano de
    copyright y la forma de cita habitual en la literatura de administracion publica. No se cambio
    para no contradecir la pagina de derechos del ejemplar impreso, pero si el Docente no tiene el
    impreso delante, 2019 es la opcion respaldada por el identificador que lleva la entrada.
19. **Asimetria de una palabra clave EN/ES.** El ingles dice «conditional release» y el espanol
    «acceso condicional»; el preprint original usaba «liberacion condicional», que es el espejo
    exacto del ingles. Las dos son defendibles («liberacion condicional» tambien significa parole en
    espanol juridico), pero para indexacion bilingue conviene decidir una. Lo mismo, mas leve, con
    «learning management system» / «entorno virtual de aprendizaje»: el espejo literal («sistema de
    gestion del aprendizaje») son 5 palabras y se pasa del tope de 4 que se fijo.

### Constancia de verificacion adversarial (25 de agosto de 2026)

Lo que se comprobo ejecutando, no razonando, y su resultado:

- **Cifras.** Se extrajeron todos los numeros del cuerpo de los dos ficheros y se compararon. **Cero
  cifras nuevas**: ninguna cantidad del articulo montado falta en el preprint de partida. Las unicas
  cifras que aparecen y no estaban son numeros de referencia, anos y paginas de la bibliografia IEEE.
  Ademas se verifico la aritmetica interna: 135+14=149, 149-11=138, 4+4+1+1+1+1+1=13, 3+1+5+2=11,
  13+15=28, 15+6=21, 21+7=28, 6+7=13, 38+8+7=53, 8+1+1+1+1+6=18. Todas cuadran.
- **Referencias.** Los 18 DOIs del fichero (17 en la lista + el repuesto R1) devuelven **302 en
  doi.org, ninguno 404**. Ademas se comparo la ficha de Crossref de cada uno con lo que dice la
  entrada: autores, ano, volumen, numero, paginas y revista **coinciden en los 18**. Las 6 URLs sin
  DOI devuelven **200** y se confirmo su contenido (titulo y autor) salvo la de Murdoch, que es una
  SPA: para esa se confirmo por OpenAlex (Dougiamas y Taylor, 2003, pp. 171-178) y por la redireccion
  al registro esploro del mismo trabajo. DBLP confirma ademas «70:1-70:41» para [2] —o sea que
  «art. no. 70, pp. 1-41» es exacto— y pp. 159-172 para [1].
- **Las dos afirmaciones de codigo fuente.** Se descargo el fichero real
  `mod/feedback/mod_form.php` de la rama `MOODLE_405_STABLE`: la validacion contiene una sola
  comprobacion de fechas y es `$data['timeclose'] < $data['timeopen']` (estricta: la igualdad pasa),
  y los `date_time_selector` de `timeopen` y `timeclose` estan en lineas consecutivas. **Las
  Secciones 3.4 y 3.6 dicen la verdad literal.**
- **Citas.** Cero citas en formato (Autor, ano) o Autor (ano). Las 25 referencias se citan todas en
  el cuerpo (cero huerfanas) y ninguna cita apunta a una referencia inexistente. Las 8 menciones
  narrativas de autor llevan corchete.
- **Cuentas.** Titulo EN 11 palabras, titulo ES 12; abstract 249 palabras, resumen 249; 5 palabras
  clave por idioma, ninguna por encima de 4 palabras; 25 referencias numeradas 1..25 sin huecos ni
  repetidos; 5 tablas, 0 figuras.
- **Tablas.** Las 40 lineas de tabla del articulo son **byte a byte identicas** a las del preprint.
- **Conclusiones.** Se comparo la Seccion 6 vieja con la nueva afirmacion por afirmacion: ninguna
  cambia de sentido. Lo que se anade (los hallazgos sobre el propio instrumento, el parrafo del
  segundo eje) reutiliza cifras que ya estaban en las Secciones 3.7, 4.2 y 4.3.
- **El original no se toco.** `git hash-object` del preprint da el mismo blob que HEAD
  (`c31760be1a8fd598dec6da4a1fa989731a77970d`) y su fecha de modificacion sigue siendo la del 23 de
  agosto.
- **Corregido en esta pasada.** La nota sobre identificadores decia que los ids de Moodle «se han
  sustituido por etiquetas neutras» y que la sustitucion es «uno a uno y consistente», cuando las
  tablas conservan los course ids y los `cmid` a proposito —y la declaracion de disponibilidad de
  datos dice que se conservan justamente para que los administradores reproduzcan las lecturas. Era
  una contradiccion interna heredada del preprint; la nota se reescribio para describir lo que el
  articulo hace de verdad. No se movio ninguna cifra.
