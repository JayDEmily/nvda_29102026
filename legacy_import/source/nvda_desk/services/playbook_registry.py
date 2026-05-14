"""Checked-in playbook registry loading and lookup helpers."""

from __future__ import annotations

from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.schemas.playbook_registry import (
    ExecutionTemplateSpec,
    PlaybookFamilySpec,
    PlaybookRegistryDocument,
    PlaybookSpec,
    SetupVariantSpec,
)


class PlaybookRegistryService:
    """Load and expose the checked-in playbook registry deterministically.

    Purpose:
        Make live playbook, family, setup-variant, and execution-template lookup
        come from the checked-in registry.
    Inputs:
        Optional registry path override; otherwise uses
        `Settings.playbook_registry_path`.
    Outputs:
        Typed playbook ordering plus family, setup-variant, and execution-template
        lookup surfaces.
    Determinism:
        Loads one checked-in YAML file with no live calls or hidden fallbacks.
    """

    def __init__(self, registry_path: Path | str | None = None):
        if registry_path is None:
            registry_path = Settings().playbook_registry_path
        self._registry_path = Path(registry_path)
        self._document: PlaybookRegistryDocument | None = None

    def document(self) -> PlaybookRegistryDocument:
        """Return the cached typed registry document."""

        if self._document is None:
            self._document = PlaybookRegistryDocument.from_yaml_path(self._registry_path)
        return self._document

    def ordered_playbooks(self) -> list[PlaybookSpec]:
        """Return active playbooks in deterministic registry priority order."""

        return self.document().ordered_playbooks()

    def ordered_setup_variants(self) -> list[SetupVariantSpec]:
        """Return active setup variants in deterministic registry priority order."""

        return self.document().ordered_setup_variants()

    def active_playbook_ids(self) -> list[str]:
        """Return active playbook ids in deterministic priority order."""

        return [playbook.playbook_id for playbook in self.ordered_playbooks()]

    def active_setup_variant_ids(self) -> list[str]:
        """Return active setup-variant ids in deterministic priority order."""

        return [variant.setup_variant_id for variant in self.ordered_setup_variants()]

    def playbook_index(self) -> dict[str, PlaybookSpec]:
        """Return deterministic playbook lookup by id."""

        return {playbook.playbook_id: playbook for playbook in self.document().playbooks}

    def family_index(self) -> dict[str, PlaybookFamilySpec]:
        """Return deterministic family lookup by id."""

        return self.document().family_index()

    def setup_variant_index(self) -> dict[str, SetupVariantSpec]:
        """Return deterministic setup-variant lookup by id."""

        return self.document().setup_variant_index()

    def template_index(self) -> dict[str, ExecutionTemplateSpec]:
        """Return deterministic execution-template lookup by id."""

        return self.document().execution_template_index()

    def playbook(self, playbook_id: str) -> PlaybookSpec:
        """Return one playbook spec by id."""

        return self.playbook_index()[playbook_id]

    def family(self, family_id: str) -> PlaybookFamilySpec:
        """Return one playbook family by id."""

        return self.family_index()[family_id]

    def setup_variant(self, setup_variant_id: str) -> SetupVariantSpec:
        """Return one setup variant by id."""

        return self.setup_variant_index()[setup_variant_id]

    def playbooks_for_setup_variant(self, setup_variant_id: str) -> list[PlaybookSpec]:
        """Return active playbooks linked to one setup variant in priority order."""

        return [
            playbook
            for playbook in self.ordered_playbooks()
            if playbook.setup_variant_id == setup_variant_id
        ]

    def active_playbook_ids_for_setup_variant(self, setup_variant_id: str) -> list[str]:
        """Return active playbook ids linked to one setup variant in priority order."""

        return [
            playbook.playbook_id for playbook in self.playbooks_for_setup_variant(setup_variant_id)
        ]

    def template(self, template_id: str) -> ExecutionTemplateSpec:
        """Return one execution template by id."""

        return self.template_index()[template_id]

    def template_for_playbook(self, playbook_id: str) -> ExecutionTemplateSpec:
        """Return the execution template linked to one playbook id."""

        playbook = self.playbook(playbook_id)
        template_id = playbook.execution_expression_id or playbook.execution_template_id
        return self.template(template_id)

    def family_for_playbook(self, playbook_id: str) -> PlaybookFamilySpec:
        """Return the owning family for one playbook id."""

        return self.family(self.playbook(playbook_id).family_id)

    def setup_variant_for_playbook(self, playbook_id: str) -> SetupVariantSpec:
        """Return the owning setup variant for one playbook id."""

        return self.setup_variant(self.playbook(playbook_id).setup_variant_id)
