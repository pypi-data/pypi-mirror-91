
import React from 'react'
import L from 'react-dom-factories'
L_ = React.createElement

export default Vis = ({data, setattr})->
    {addr} = data
    if not data?.addr
      return 'Loading...'
    addr = addr
    L.div style:display:'contents',
        L.iframe src:addr
