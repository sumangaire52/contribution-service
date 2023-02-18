# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2022-2023 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains the shared state for the abci skill of DynamicNFTAbciApp."""

from typing import Any

from packages.valory.skills.abstract_round_abci.models import BaseParams
from packages.valory.skills.abstract_round_abci.models import (
    BenchmarkTool as BaseBenchmarkTool,
)
from packages.valory.skills.abstract_round_abci.models import Requests as BaseRequests
from packages.valory.skills.abstract_round_abci.models import (
    SharedState as BaseSharedState,
)
from packages.valory.skills.dynamic_nft_abci.rounds import DynamicNFTAbciApp


class SharedState(BaseSharedState):
    """Keep the current shared state of the skill."""

    abci_app_cls = DynamicNFTAbciApp

    def setup(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the state."""
        super().setup(*args, **kwargs)


class Params(BaseParams):
    """Parameters."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the parameters object."""
        self.ipfs_domain_name = self._ensure("ipfs_domain_name", kwargs, str)
        leaderboard_base_endpoint = self._ensure(
            "leaderboard_base_endpoint", kwargs, str
        )
        leaderboard_sheet_id = self._ensure("leaderboard_sheet_id", kwargs, str)
        self.leaderboard_points_range = self._ensure(
            "leaderboard_points_range", kwargs, str
        )
        self.leaderboard_layers_range = self._ensure(
            "leaderboard_layers_range", kwargs, str
        )
        leaderboard_api_key = self._ensure("leaderboard_api_key", kwargs, str)
        leaderboard_params = self._ensure("leaderboard_param_template", kwargs, str)
        leaderboard_params.replace(
            "<leaderboard_layers_range>", self.leaderboard_layers_range
        )
        leaderboard_params.replace(
            "<leaderboard_points_range>", self.leaderboard_points_range
        )
        leaderboard_params.replace("<leaderboard_api_key>", leaderboard_api_key)
        self.leaderboard_endpoint = f"{leaderboard_base_endpoint}/{leaderboard_sheet_id}/values:batchGet?{leaderboard_params}"
        self.whitelist_api_key = kwargs.pop("whitelist_api_key", None)
        self.whitelist_endpoint = self._ensure("whitelist_endpoint", kwargs, str)
        self.dynamic_contribution_contract_address = self._ensure(
            "dynamic_contribution_contract_address", kwargs, str
        )
        self.token_uri_base = self._ensure("token_uri_base", kwargs, str)
        self.ipfs_gateway_base_url = self._ensure("ipfs_gateway_base_url", kwargs, str)
        self.basic_image_cid = self._ensure("basic_image_cid", kwargs, str)
        self.earliest_block_to_monitor = self._ensure(
            "earliest_block_to_monitor", kwargs, int
        )

        super().__init__(*args, **kwargs)


Requests = BaseRequests
BenchmarkTool = BaseBenchmarkTool
