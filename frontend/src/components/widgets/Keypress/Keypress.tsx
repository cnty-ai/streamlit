/**
 * @license
 * Copyright 2018-2021 Streamlit Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import React, { ReactElement, useEffect } from "react"
import { Keypress as KeypressProto } from "src/autogen/proto"
import { WidgetStateManager } from "src/lib/WidgetStateManager"

export interface Props {
  disabled: boolean
  element: KeypressProto
  widgetMgr: WidgetStateManager
  width: number
}

function Keypress(props: Props): ReactElement {
  const { disabled, element, widgetMgr, width } = props

  useEffect(() => {
    // Listen for any keypress in the entire application
    const eventListenerFunction = (e: KeyboardEvent) => {
      widgetMgr.setStringValue(element, e.key, {
        fromUi: true,
      })
    }

    document.addEventListener("keypress", eventListenerFunction, false)
    return () => {
      document.removeEventListener("keypress", eventListenerFunction, false)
    }
  }, [])

  // This isn't a visual component
  return <></>
}

export default Keypress
