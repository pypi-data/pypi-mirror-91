import React, { Component, useState } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement

export default class ErrorBoundary extends Component
  constructor:(props)->
    super(props)
    @state = error:null

  componentDidCatch:(error, errorInfo)->
    e = error:error, info:errorInfo
    console.log 'error boundary catched:', e
    @setState error: error:error, info:errorInfo

  render:()->
    console.log @state.error if @state?.error
    if @state.error?.error
      L.div className:'error-module',
        L.span  0, 'Error:'
        L.span className:'error-message',
          @state.error.error.message
        L.div className:'error-data',
          L.p 0, 'Type:', @props.type
          L.p 0, 'Value:'
          L.textarea 0, JSON.stringify @props.value
        L.p 0,'JS stacktrace:'
        L.textarea className:'error-stack',
          @state.error.error.stack
        L.p 0,'Component stacktrace:'
        L.textarea className:'error-stack',
          @state.error.info.componentStack
    else
      @props.children
