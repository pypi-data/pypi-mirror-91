export {default as LineGraph} from './lineGraph_recharts.coffee'
export {default as sys_Image} from './sys_Image.coffee'
export {default as MplD3} from './mpld3.coffee'
export {default as Raw} from './Raw.coffee'

import {wrapModuleWithLegimens} from "./LeWidget.coffee"

// installed modules, generated automatically
import * as installed from "./installed"

var x = {}

for (let key of Object.keys(installed)) {
    x[key] = wrapModuleWithLegimens( installed[key] );
    console.log(x)
    }
export {x as installed}
