import React, { Component, useState } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement

import Input from 'modules/UIcomponents/input.coffee'
import Button from 'modules/UIcomponents/button.coffee'
import checkedIcon from './checked.svg'
import brokenLinkIcon from './broken-link.svg'
import styles from './styles.less'


export default topbar=({addr, addWidget, addrChange, connected})=>
    L.div className:'top-bar',
      L.div className:'address inline',
        L_ Input,
          value: addr
          onChange: addrChange
        L_ statusBadge, isConnected:connected
      L_ Button,
        className: 'add-widget'
        text: 'Add widget'
        onPress: addWidget

statusBadge = ({isConnected}) ->
  [displayHover, setDisplayHover] = useState(false)

  L.span
    className: 'status'
    onMouseEnter: ()=>setDisplayHover true
    onMouseLeave: ()=>setDisplayHover false
    L.img className:'connected-icon', src: if isConnected then checkedIcon else brokenLinkIcon
    L.span
      className:'popup'
      style:
        maxWidth: if displayHover then 200 else 100
        maxHeight: if displayHover then 130 else 0
        opacity: if displayHover then .9 else 0.0
        transitionDuration: '150ms'
        transitionProperty: 'max-width max-height opacity'
        overflow: 'hidden'
      if isConnected then 'Connected!' else 'Disconnected! If Libvis Websocket server is already running, try reloading the page. Also, make sure you use the same ws_address as the server.'

