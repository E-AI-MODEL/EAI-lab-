# Architecture

## 1. Semantic authority

EAI Core 0.5.4 is bundled under `src/eai_lab/core/` and is treated as read-only semantic authority. Application code may expose or execute the core, but must not silently simplify, average or replace its states, gates, evidence rules or `UNKNOWN` semantics.

## 2. Three kinds of state

### Observed state

The event log records what was observable: who acted, in which phase, what action occurred and which target operation was involved.

### Derived state

Future reducers may derive hypotheses or classifications from those events. Derived state must keep links to its source event IDs and may remain unknown.

### Synthetic state

Simulation state is separate. A simulator may contain hidden or latent variables for benchmarking, but those variables are not evidence about a real learner and are not automatically visible to the EAI runtime.

## 3. Hard boundary: real versus simulation

`EventStore(namespace="real")` accepts only events with `synthetic=false`.
`EventStore(namespace="simulation")` accepts only events with `synthetic=true`.

This is the first technical guard against a common category error: treating generated learner behavior as measured learner behavior.

## 4. Append-only evidence

Events are immutable observations. New interpretations create new evidence records; they do not rewrite the original event.

```text
observable action
    -> learning_event
    -> event store
    -> evidence record
    -> EAI classification/gates
    -> bounded claim or intervention decision
```

## 5. Cognitive work remains attributable

Every learning event has an actor. This lets later runtime logic reconstruct whether the target operation was performed by the learner, AI, teacher, peer or a combination.

## 6. No universal mastery number

The foundation deliberately does not expose a single mastery percentage. Independence, retention and transfer are distinct evidence questions and require different observations.

## 7. Next runtime layer

The next code layer will add deterministic routing and gate evaluation, candidate intervention objects, support fading, independent retry and transfer probes, evidence-backed learner-state reducers, and a simulation harness with latent-vs-observed separation.

Generative models may propose actions. They do not get authority to declare mastery or rewrite evidence.
