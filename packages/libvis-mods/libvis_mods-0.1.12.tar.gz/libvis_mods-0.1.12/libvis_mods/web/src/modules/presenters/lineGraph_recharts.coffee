import React, { Component } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement
import {LineChart, Line,
XAxis, YAxis,
ResponsiveContainer, CartesianGrid} from 'recharts'

transpose_01 = (obj)->
  """
  Take object {
                a: [a_i], 
                b: [b_i], ...
              }
  and convert to [
                  {a:a_0, b:b_0}, 
                  {a:a_1, b:b_1}, ... 
                ]
  Works also for [ [a_i], [b_i] ]
  since array is an object with int keys
  """
  
  k1 = Object.keys obj
  elem = obj[k1[0]]
  k2 = Object.keys elem
  len2 = k2.length
  result = {}

  # set up a dict
  for key in k2
    result = Object.assign result, [key]:{}

  for j in [0..(len2-1)]
    result[j] = {}
    for i in k1
      result[j][i] = obj[i][j]
  result


#export default class Vis extends React.Component
export default Vis = (props)->
  {labelDim, domainLabel, data} = props
  if not labelDim
    labelDim = 0

  keys = Object.keys data
  if typeof (data[keys[0]]) != 'object'
    data = y:data, x:[0..(keys.length-1)]
    domainLabel='x'

  keys = Object.keys data


  if labelDim==0
    if Array.isArray data
      domainLabel = '0'
    data = transpose_01 data
  if labelDim==1
    elem = data[keys[0]]
    keys = Object.keys elem

  data_keys = keys.filter (k)-> k!=domainLabel

  #convert to array
  data = Object.keys(data).map (d)->data[d]

  render_dots = data.length < 30
  colors = ["#e41a1c",
            "#377eb8",
            "#4daf4a",
            "#984ea3",
            "#ff7f00",
            "#ffff33",
            "#a65628",
            "#f781bf",
            "#999999"]
  colors_count = 9
  current_color = -1

  L.div className:'flex-col graph',
    #console.debug 'chart data', data, domainLabel
    L_ ResponsiveContainer,
      width:"99%"
      height:"97%" # Magic value: sometimes 100% triggers overflow
      L_ LineChart,
        data: data
        margin: {top: 2, right: 8, left: -20, bottom: 2}
        L_ XAxis,
          dataKey: domainLabel
          type: 'number'
          stroke: '#333'
          # Log base 10 using conversion to string
          #interval: Math.pow(10, (""+data.length).length-2)-1
        L_ YAxis, domain: ['auto', 'auto'], stroke:'#333'
        L_ CartesianGrid, stroke:'#eee'
        for k in data_keys
          if current_color<= colors_count
            current_color += 1
          L_ Line,
            key: k
            stroke: colors[current_color]
            type: "linear"
            animationDuration: 200
            dot: render_dots
            dataKey: k
