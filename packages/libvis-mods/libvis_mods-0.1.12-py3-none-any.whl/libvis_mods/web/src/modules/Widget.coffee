import Input from './UIcomponents/input.coffee'
import React, { Component, useState } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement

withDeleteButton = (onDelete, children)->
  L.div className:'contents',
    L.div
      className:'delete-card'
      onClick:onDelete
      'x'
    children

withName = ({name, onNameChange, children})->
  [nameHidden, setNameHidden] = useState(false)
  toggle = (()=>setNameHidden !nameHidden)
  L.div className:'contents',
    if !nameHidden
      L.div className:'title',
        L.label onClick:toggle, "vis.vars."
        L_ Input, value:name, onChange:onNameChange
    else
      L.div className:'title-hidden', onClick:toggle
    children

export default Widget = (props, children)->
  {variable, name, onNameChange, onDelete} = props
  L.div className:'widget', key:props.key,
    withDeleteButton onDelete,
      L_ withName, name:name, onNameChange:onNameChange,
        L.div className:'widget-contents',
          children
