import React, { Component } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement
import Input from './UIcomponents/input.coffee'
import ErrorBoundary from './error_boundary.coffee'
import * as Modules_def from './presenters'
import { installed } from './presenters'

Modules = { Modules_def..., installed... }
console.log(Modules)

get_var_type = (type, val)->
  #console.log 'in get_var_type', type
  if type=='mpl'
    return 'MplD3'
  if type=='_img'
    return 'sys_Image'
  if val is null
    return 'Raw'
  try
    if val.length>10
      if val[0].length>10
        return 'Image'
  catch
  if Array.isArray(val)
    return 'LineGraph'
  if type=='raw'
    return 'Raw'
    
  return type

export choosePresenter = (type, val)->
  type = get_var_type type, val
  #console.debug "Modules dict:", Modules
  presenter = Modules[type]
  if not presenter
    presenter = Modules['Raw']
  console.debug "Using presenter #{presenter.constructor.name} for '#{type}'"
  return presenter

export LibvisModule = ({object, addr})->
  if object is undefined
    type= 'Raw'
    value = null
  else
    {type, value} =  object

  Pres = choosePresenter type, value
  L.div className:"libvismod vistype-#{type}",
    L_ ErrorBoundary, type:type,value:value,
      L_ Pres, data:value, addr:addr
