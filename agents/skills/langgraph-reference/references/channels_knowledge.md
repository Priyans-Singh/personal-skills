# `channels/`

State-field storage and merge semantics used by the engine. `BaseChannel` is the contract; `LastValue` is ordinary single-value state; `BinaryOperatorAggregate` applies a reducer; `Topic` collects pub/sub values; `NamedBarrierValue` waits for named upstream writes. `AnyValue`, `DeltaChannel`, `EphemeralValue`, and `UntrackedValue` cover advanced retention/versioning rules. Choose reducers through state annotations rather than importing these directly unless writing engine-level code.
