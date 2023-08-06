import React, { Component } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement

import useLegimens from 'legimens'

export wrapModuleWithLegimens = (Pres) => ({data, addr}) =>
  {data, status, respond} = useLegimens {addr, ref:data}
  variable=data
  setattr=respond
  #console.debug "in wrapper of variable", variable
  setattr = (key, value) ->
    respond JSON.stringify [key]:value
  if variable is undefined
    variable = value:'Loading', type:'raw'
    content = "Loading"
  else
    content = L_ Pres, data:variable, addr:addr, setattr:setattr

  L.div className:'contents', content

