<script>
  import { LayerCake, Svg, Html } from 'layercake';
  import { scaleOrdinal } from 'd3-scale';
   import { scaleLog, scaleBand } from 'd3-scale';

  import MultiLine from './components/MultiLine.svelte';
  import AxisX from './components/AxisX.svelte';
  import AxisY from './components/AxisY.svelte';
  import AxisYLog from './components/AxisYLog.svelte';
  import Labels from './components/Labels.svelte';
  import Tooltip from './components/Tooltip.svelte';
  import MultiTooltip from './components/MultiTooltip.svelte';
  import QuadTree from './components/QuadTree.svelte';
  import AxisYScaleBand from './components/AxisYScaleBand.svelte';
  import Bar from './components/Bar.svelte';

  import MapScale from './components/MapScale.svelte';
  import AxisXScaleBand from './components/AxisXScaleBand.svelte';
 

  import { feature } from 'topojson';
  //import usStates from './data/us-states.topojson.js';
  import ORCounties from './data/orcounties.js';

  import { onMount } from 'svelte';

  import MapSvg from './components/MapSvg.svelte';
  const geojson = feature(ORCounties, ORCounties.objects.reprojection);


  /* data */
  import coviddata from './data/coviddata.js'
  import hospitalizeddata from './data/everhospitalized.js'





  let bar_chart_case_data = []
  let region_pop_data = {}

  let dead_v_cases;  // Only do this for the whole state. 


  let dead_v_cases_long
  let dead_v_cases_series;
  let dead_v_cases_domain;


  let dead_v_cases_colorScale;

  let state_rate_dict = {};

  let max_date_string;

var labels = [
    {'label':'0'},
    {'label':'<299'},
    {'label':'<399'},
    {'label':'<499'},
    {'label':'<599'},
    {'label':'600+'}

  ]
  var label_array = [];

  labels.forEach(row => {
    row.value = 1;
    label_array.push(row.label);
  });

  const map_colors = ['#ffffff', '#feedde', '#fdbe85','#fd8d3c','#e6550d','#a63603'];

  let results_for_table = [];

  function format_number(num) {
    var num_raw = num.toLocaleString()
    var num_parts = num_raw.toString().split(".");
    num_parts[0] = num_parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return num_parts.join(".");
  }

  function format_rate(num) {
    return parseFloat(num.toFixed(1));
  }

  function format_date_string(this_date_string) {
    var dsparts = this_date_string.split("_");
    var result = String(parseInt(dsparts[1])) + "/" + dsparts[2];
    return result;
  }

  function prep_data_from_archive(data_type, fips) {

    var data_for_this_fips = [];
    var this_jurisdiction = coviddata[fips];
    var day_count = 0;
    Object.keys(this_jurisdiction).sort().forEach(function(key) {
      if (key.startsWith('2020')) {
        day_count += 1;
        var key_parts = key.split("_")

        var month = parseInt(key_parts[1]);
        var year = parseInt(key_parts[0]);
        var day = parseInt(key_parts[2]);

        if (key > max_date_string || !max_date_string) {
          max_date_string = key;
        }

        // javascript has a month implementation bug
        var this_date = new Date(year, month-1, day);
      
        if (data_type == 'cases') {
          var case_count = this_jurisdiction[key]['c'];
          if (case_count < 0) {
              case_count = 0;
            }
          if (case_count > 0) {
            data_for_this_fips.push({'month':this_date, 'Cases':case_count});
          }
        }
        if (data_type == 'new_cases') {
          var new_case_count = this_jurisdiction[key]['n_c'];
          if (new_case_count < 0) {
            // When they move cases to another county you can get negatives
            new_case_count = 0;
          }
          // we don't have 'new' cases on day 1
          if (day_count > 1)  {
            data_for_this_fips.push({'month':this_date, 'New Cases':new_case_count});
          }
        }
        if (data_type == 'deaths') {
          var death_count = this_jurisdiction[key]['d'];
          data_for_this_fips.push({'month':this_date, 'Deaths':death_count});
        }

        if (data_type == 'tests') {
          if (day_count > 2)  {
            data_for_this_fips.push({'month':this_date, 'Negatives':this_jurisdiction[key]['n_n'], 'Positives':this_jurisdiction[key]['n_c']});
          }
        }

        if (data_type == 'new_deaths') {

          if (day_count > 1)  {
            var new_death_count = this_jurisdiction[key]['n_d'];
            // Don't show less than zero
            // This happens if they retrospectively move a death
            if (new_death_count < 0) {
              new_death_count = 0;
            }
            data_for_this_fips.push({'month':this_date, 'New Deaths':new_death_count});
          }
        }
        if (data_type == 'dead_v_cases') {
          var this_data = {'month':this_date};

          if (this_jurisdiction[key]['d'] > 0 && this_jurisdiction[key]['c']) {
            data_for_this_fips.push({'month':this_date, 'Deaths':this_jurisdiction[key]['d'], 'Cases':this_jurisdiction[key]['c']});
          }
        }
      }
    });
    return data_for_this_fips;
    
  }

 /* --------------------------------------------
   * Set what is our x key to separate it from the other series
   */
  const xKey = 'month';
  
  var seriesColors = [
    '#00a2e3',
    '#b71f24',
    '#e09d1f',
    '#84878b',
  ];

  // could simplify this
  var barColors = [
    '#00a2e3',
    '#00a2e3',
    '#00a2e3',
  ];


  function get_long_data(data) {
    const data_long = Object.keys(data[0]).map(key => {
      if (key === 'month') return null;
      return {
        key,
        values: data.map(d => {
          return { key, month: d[xKey], value: d[key] };
        })
      };
    }).filter(d => d);
    return data_long

  }

  // Todo: expand all the arrow functions 
  const flatten = thisdata => thisdata.reduce((store, group) => store.concat(group.values), []);

  const monthNames = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.'];


  function get_series_names(data) {
    var this_series_names = Object.keys(data[0]).filter(d => d !== xKey);
    return this_series_names;
  }

  // We can usually let layercake's default handle this? 
  function get_domain(longdata, is_log) {
    var max_value = 2;
    var min_value = undefined;

    for (var i=0; i<longdata.length; i++) {


      for (var j=0; j<longdata[i]['values'].length; j++) {

        if (longdata[i]['values'][j]['value'] > max_value) {
          max_value = longdata[i]['values'][j]['value'];
        }
        if (longdata[i]['values'][j]['value'] < min_value || min_value == undefined ) {
            min_value = longdata[i]['values'][j]['value'];
        }
      }
    }
    if (is_log ) {
      min_value = 1;
    }
    if (!is_log) {
      min_value = 0;
    }
    var interval = [min_value, max_value];
    return interval;
  }

  function set_sitewide_charts(){
    //Run this once, these are not regenerated
    dead_v_cases = prep_data_from_archive('dead_v_cases', '41000');
    dead_v_cases_long = get_long_data(dead_v_cases);
    dead_v_cases_series = get_series_names(dead_v_cases);
    dead_v_cases_domain = get_domain(dead_v_cases_long,true);

    dead_v_cases_colorScale = scaleOrdinal()
      .domain(dead_v_cases_series)
      .range(seriesColors);

    var portland_cases = coviddata['38900'][max_date_string]['c'];
    var salem_cases = coviddata['41420'][max_date_string]['c'];
    var ros_cases = coviddata['41000'][max_date_string]['c'] - portland_cases - salem_cases;

    bar_chart_case_data.push({'name':'Rest of state','cases':ros_cases})
    bar_chart_case_data.push({'name':'Salem Area','cases':salem_cases})
    bar_chart_case_data.push({'name':'Portland Area','cases':portland_cases})

    region_pop_data['metro_pop'] = coviddata['38900']['pop'] + coviddata['41420']['pop'];
    region_pop_data['rest_pop'] = coviddata['41000']['pop'] - region_pop_data['metro_pop'];  
  }

  set_sitewide_charts();

  function get_state_rates() {
    Object.keys(coviddata).forEach(function(key) {
      
      var per_million_cases = 1000000 * coviddata[key][max_date_string]['c']/coviddata[key]['pop'];

      var per_million_deaths = 1000000 * coviddata[key][max_date_string]['d']/coviddata[key]['pop'];
      state_rate_dict[key] = per_million_cases;
      var is_bold = false;
      var name_formatted = coviddata[key]['name'];
      //name_formatted = name_formatted.replace('County', 'Cnty')

      if (key == '41000' || key == '41420' || key=='38900') {
        name_formatted = "<b>" + name_formatted + "</b>"
      }
      var this_row = {
        name: name_formatted,
        pop: parseInt(coviddata[key]['pop']),
        cpm: per_million_cases,
        dpm: per_million_deaths,
      }
      results_for_table.push(this_row);
    });
    results_for_table.sort((a, b) => (a.cpm < b.cpm) ? 1 : -1)
  }

  get_state_rates();


function set_fill(featureid) {
    
    var rate = state_rate_dict[featureid];
    if (rate == 0) {
      return map_colors[0];
    }
    if (rate < 300) {
      return map_colors[1];
    }
    if (rate < 400) {
      return map_colors[2];
    }
    if (rate < 500) {
      return map_colors[3];
    }
    if (rate < 600) {
      return map_colors[4];
    }
    return map_colors[5];
  }


  function formatTickX (d) {
    const date = new Date(d);
    var day = date.getDate();
    if (day%5==0) {
      return `${monthNames[date.getUTCMonth()]} ${date.getUTCDate()}`;
    } else {
      return '';
    }
  }
  
  function formatTickY (d) {
    if (d > 999) {
      return d / 1000 + 'k';
    }
    return d;
  }

  
</script>

<style>

.scale_container {
  margin-top:30px;
  width: 80%;
  max-width: 400px;
  height: 30px;
}

table {
  border-collapse: collapse;
  border-spacing: 0;
  width: 100%;
  border: 1px solid #ddd;
}

th, td {
  text-align: left;
  padding: 10px;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}

.cshead {
   background-color: #f2f2f2;
}
</style>


<div class="title">
  <h3>Cases by Region</h3>
</div>
  <div class="chart-container-short">
  <LayerCake
    padding={{ top: 0, bottom: 20, left: 80, right: 20, }}
    x='cases'
    y='name'
    yScale={scaleBand().paddingInner([0.05]).round(true)}
    yDomain={['Rest of state', 'Salem Area', 'Portland Area']}
    xDomain={[0, null]}
    data={bar_chart_case_data}
  >
    <Svg>
      <AxisX
        gridlines={true}
        baseline={true}
        snapTicks={true}
      />
      <AxisYScaleBand gridlines={false}/>
      <Bar
        colorScale={barColors}
      />
    </Svg>
  </LayerCake>
</div>

<div class="title">
<h3>Total Deaths and Cases</h3>
</div>

<div class="chart-container">
  <LayerCake
    padding={{ top: 27, right: 10, bottom: 20, left: 40 }}
    x='month'
    y='value'
    flatData={flatten(dead_v_cases_long)}
    yDomain={[1, null]}
  yScale={scaleLog()}
    data={dead_v_cases_long}
  >
    <Svg>
      <AxisX
        gridlines={false}
        ticks={dead_v_cases.map(d => d[xKey])}
        formatTick={formatTickX}
        snapTicks={true}
      />
      <AxisYLog
        formatTick={formatTickY}
      />
      <MultiLine
        colorScale={dead_v_cases_colorScale}
      />
    </Svg>

    <Html>
      <Labels/>
      <MultiTooltip
        dataset={ dead_v_cases }
      />
    </Html>
  </LayerCake>
  </div>
<p>Explainer text</p>

<div class="title">
<h3>Infection Rate by County</h3>
</div>

<div class="chart-container">
  <LayerCake
    data={geojson}
  >
    <Svg>
      <MapSvg
        projectionName={'geoMercator'}
        {set_fill}
      />
    </Svg>
  </LayerCake>
</div>


<div class="scale_container">
  <LayerCake
      padding={{ top: 0, right: 0, bottom: 20, left:20 }}
      x='label'
      y='value'
      xScale={scaleBand().paddingInner([0.02]).round(true)}
      xDomain={label_array}
      yDomain={[0, null]}
      data={labels}
  >
    <Svg>
      <MapScale
      colors={map_colors}/>
      <AxisXScaleBand
        gridlines={false}
      />

    </Svg>
  </LayerCake>
  <div style="margin-left:30px;">
  <p class="byline">Scaled by the number of cases per million</p>
</div>
</div>

<div class="data-container" style="margin-top:30px;">
<h2>County Summary</h2>

<p>Rates are expressed per <b>million</b> residents.</p>
<table class="countysummary">
       <thead>
          <tr class="csrowheader">
            <th class="cshead">Area</th>
            <th class="cshead">Size</th>
            <th class="cshead">Case Rate</th>
          </tr>
        </thead>
    <tbody>
      {#each results_for_table as region}
      <tr class="csrow">
        <td class="cscell">{@html region.name}</td>
        <td class="cscell">{format_number(region.pop)}</td>
        <td class="cscell">{format_rate(region.cpm)}</td>
      </tr>
      {/each}
    </tbody>
  </table>
</div>

<div class="data-container">
<p class="byline"><b>Sources:</b> Population estimates as of July, 1 2019, <a href="https://www.pdx.edu/prc/population-reports-estimates">PSU</a>. Case and deaths are from the <a href="https://govstatus.egov.com/OR-OHA-COVID-19">Oregon Health Authority</a>. 
<br><b>Notes:</b> Dates of "new cases" reflect the day they were announced, not the day the individual became symptomatic. </p>
</div>