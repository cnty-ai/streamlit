# Copyright 2018-2021 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io

from streamlit.type_util import Key, to_key
from typing import cast, Optional, Union, BinaryIO, TextIO
from textwrap import dedent

import streamlit
from streamlit.errors import StreamlitAPIException
from streamlit.proto.Keypress_pb2 import Keypress as KeypressProto
from streamlit.in_memory_file_manager import in_memory_file_manager
from streamlit.state.session_state import (
    WidgetArgs,
    WidgetCallback,
    WidgetDeserializer,
    WidgetKwargs,
)
from streamlit.state.widgets import register_widget
from .form import current_form_id, is_in_form
from .utils import check_callback_rules, check_session_state_rules


FORM_DOCS_INFO = """

For more information, refer to the
[documentation for forms](https://docs.streamlit.io/library/api-reference/control-flow/st.form).
"""


class KeypressMixin:
    def keypress(
        self,
        args: Optional[WidgetArgs] = None,
        kwargs: Optional[WidgetKwargs] = None,
        *,  # keyword-only arguments:
        disabled: bool = False,
    ) -> str:
        key = to_key(None)
        check_callback_rules(self.dg, None)
        check_session_state_rules(default_value=None, key=key, writes_allowed=True)

        # It doesn't make sense to create a button inside a form (except
        # for the "Form Submitter" button that's automatically created in
        # every form). We throw an error to warn the user about this.
        # We omit this check for scripts running outside streamlit, because
        # they will have no report_ctx.
        if streamlit._is_running_with_streamlit:
            if is_in_form(self.dg):
                raise StreamlitAPIException(
                    f"`st.keypress()` can't be used in an `st.form()`.{FORM_DOCS_INFO}"
                )

        keypress_proto = KeypressProto()
        keypress_proto.disabled = disabled

        def deserialize_keypress(ui_value: str, widget_id: str = "") -> str:
            return ui_value or ""

        current_value, _ = register_widget(
            "keypress",
            keypress_proto,
            user_key=key,
            # on_change_handler=on_click,
            args=args,
            kwargs=kwargs,
            deserializer=deserialize_keypress,
            serializer=str,
        )
        self.dg._enqueue("keypress", keypress_proto)
        return cast(str, current_value)

    @property
    def dg(self) -> "streamlit.delta_generator.DeltaGenerator":
        """Get our DeltaGenerator."""
        return cast("streamlit.delta_generator.DeltaGenerator", self)
