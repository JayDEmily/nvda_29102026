# Extension and Retirement Rules

## Admission

A new runtime module is admitted by:

1. allocating the next unused `M` identifier;
2. defining one semantic responsibility and explicit exclusions;
3. declaring inputs, outputs, state/time/side-effect ownership and permitted dependencies;
4. generating owner-local files from the module template;
5. declaring one typed public seam;
6. admitting vocabulary and normative propositions;
7. admitting exact architecture and behavioural proof;
8. composing it through the application shell;
9. passing the aggregate promotion gate.

The same lifecycle applies to other categories with category-appropriate implementation requirements. A protocol, governance plane or surface does not require a runtime package merely because it is registered.

## Replacement, split and merger

A replacement, split or merger must preserve:

- predecessor identifiers;
- successor identifiers;
- semantic migration statement;
- compatibility impact;
- consumer migration status;
- proof and vocabulary dispositions.

No successor silently inherits implementation status or authority.

## Deprecation and retirement

A deprecated object is unavailable for new composition and carries an explicit retirement path. A retired object is absent from composition and its identifier remains permanently reserved.

Git history preserves deleted implementation. The active tree must not contain a second archive copy.
