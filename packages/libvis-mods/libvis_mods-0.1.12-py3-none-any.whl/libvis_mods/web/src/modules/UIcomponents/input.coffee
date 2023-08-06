import React, { Component } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement
get_style = (value)->
  width:value?.length*9+10

export default Input = (props)->

  onChange = (event)=>
    console.log event, event.target.value
    value = event.target.value
    props.onChange value

  {value} = props
  L.input
    type:'text'
    style: get_style value
    value:    value
    onChange: onChange
