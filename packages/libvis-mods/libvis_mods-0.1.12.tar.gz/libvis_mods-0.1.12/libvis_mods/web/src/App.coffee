import React, { useState, useEffect } from 'react'
import L from 'react-dom-factories'
L_ = React.createElement

import {Responsive, WidthProvider} from 'react-grid-layout'

import useLegimens from 'legimens'
import {useLegimensRoot} from 'legimens'

import Notebook from './modules/notebook.coffee'
import {LibvisModule} from './modules/visualiser.coffee'
import ResponsiveGL from './modules/ResponsiveStorageGrid.coffee'
import Widget from './modules/Widget.coffee'
import TopBar from './modules/UIcomponents/Topbar'

import LocalStorage from './modules/helpers/localStorage.coffee'
import {get_nb_name} from './modules/helpers/argparser.coffee'
import {parse_message} from './Data/interface.coffee'

import './styles/grid.css'
import './styles/widget.less'
import './styles/graph.less'
import './styles/misc.less'
import './styles/top_bar.less'

visStorage = new LocalStorage key:'webvis'


export default App = (props) =>
  hostname = window.location.hostname
  [addr, setAddr] = useState "ws://#{hostname}:7700/"
  [widgets, setWidgets] = useState visStorage.get('widgets') or {}

  set_widgets = (widgets)=>
    console.debug 'setting widgets' , widgets
    setWidgets widgets
    visStorage.save 'widgets', widgets

  nameChange = (id)=>(name)=>
    console.log 'namechange', widgets, name, id
    widgets[id].name = name
    set_widgets {widgets..., [id]: {name, widgets[id]...}}

  addWidget= ({name})=>
    new_widget = name: (name or 'foobar')
    new_id = Date.now()
    widgets[new_id] = new_widget
    set_widgets {[new_id]:new_widget, widgets...}

  add_widgets_from = (vars) =>
    current_widgets_names = []
    for id, w of widgets
      current_widgets_names.push w.name

    for name, variable of vars
      if name not in current_widgets_names
        addWidget {name}


  deleteWidget= (id)->()=>
    console.log "Deleting widget #{id}"
    delete widgets[id]
    set_widgets {widgets...}


  _widget = (var_, name, idx) =>
    Widget
      key: idx
      onDelete: deleteWidget idx
      onNameChange: nameChange idx
      name: name
      LibvisModule object:var_, addr:addr

  _get_widgets=(vars)=>
    #nb = L.div key:'notebook', L_ Notebook, nb_name:get_nb_name()
    displayedWidgets = []

    for idx, params of widgets
      {name} = params
      variable = vars?[name] or value:'No value',type:'raw'

      displayedWidgets.push _widget variable, name, idx
    console.log 'widgets', widgets, 'displayedWidgets', displayedWidgets
    return displayedWidgets

  _grid=(vars)->
    L_ ResponsiveGL,
      className:'grid'
      draggableCancel:".container, input, textarea, .nodrag"
      _get_widgets vars

  console.log "****************"
  console.log "App render start"
  console.log "****************"
  {data, status, respond} = useLegimensRoot addr:addr
  vars = data
  console.debug 'vars', vars
  L.div className:'app',
    L_ TopBar,
      addr: addr
      addWidget: addWidget
      addrChange: setAddr
      connected: status.connected
    if not vars
      'Loading...'
    else
      add_widgets_from vars
      _grid vars
