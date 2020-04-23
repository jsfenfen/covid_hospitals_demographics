<script>
  import { LayerCake, Svg, Html } from 'layercake';
  import { scaleOrdinal } from 'd3-scale';
   import { scaleBand } from 'd3-scale';

  import MapScale from './components/MapScale.svelte';
  import AxisXScaleBand from './components/AxisXScaleBand.svelte';
  import Points from './components/Points.svelte';


  import { feature } from 'topojson';
  //import usStates from './data/us-states.topojson.js';
  import ORCounties from './data/orcounties.js';

  import { onMount } from 'svelte';

  import MapSvg from './components/MapSvg.svelte';
  const geojson = feature(ORCounties, ORCounties.objects.reprojection);


  import Chip, {Set, Icon, Text} from '@smui/chips';

  /* data */
  import coviddata from './data/coviddata.js'

  onMount(() => {
    // Assumes that pymchild is defined on the page before here! 
    pymChild.sendHeight();
  });

  let breaks =  [] 


  let bar_chart_case_data = []
  let region_pop_data = {}
  let table_choice = 'Metro Areas';

    // Hmm... https://stackoverflow.com/questions/56983938/in-svelte-how-to-console-logyes-when-a-variable-changed
  $: table_choice, handleSelect(table_choice);

  let dead_v_cases;  // Only do this for the whole state. 

  let points = [
    {'name': 'Portland',
      'prominence':3,
      'points': [
        -122.6750, // Portland
        45.5051
    ]}
    ,
    {'name': 'Salem',
    'prominence':2,
    'points':[
        -123.0351, // Salem
        44.9429
    ]},
    {'name': 'Eugene',
    'prominence':2,
    'points':[
        -123.087, 
        44.052
    ]},
    {'name': 'Bend',
    'prominence':2,
    'points':[
        -121.315, 
        44.058
    ]},
    {'name': 'Medford',
    'prominence':2,
    'points':[
        -122.876, 
        42.327
    ]},
    {'name': 'Corvallis',
    'prominence':2,
    'points':[
        -123.262, 
        44.565
    ]}
    ];

  let dead_v_cases_long
  let dead_v_cases_series;
  let dead_v_cases_domain;


  let dead_v_cases_colorScale;

  let state_rate_dict = {};

  let regions_table = [];
  let counties_table = [];

  let max_date_string;

  let labels = []
  
  var label_array = [];


  const map_colors = ['#ffffff', '#feedde', '#fdbe85','#fd8d3c','#e6550d','#a63603'];

  let results_for_table = [];

  function set_labels() {
    labels = [
      {'label':'0'},
      {'label':'<' + breaks[0]},
      {'label':'<' + breaks[1]},
      {'label':'<' + breaks[2]},
      {'label':'<' + breaks[3]},
      {'label': breaks[3] + '+'}
    ]

    labels.forEach(row => {
      row.value = 1;
      label_array.push(row.label);
    });
  }

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
          
          if (day_count > 1) {
            if (this_jurisdiction[key]['d'] > 0 && this_jurisdiction[key]['c']) {
              data_for_this_fips.push({'month':this_date, 'Deaths':this_jurisdiction[key]['d'], 'Cases':this_jurisdiction[key]['c']});
            }
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
    '#e09d1f',
    '#b71f24',
    '#00a2e3',
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

  function handleSelect() {
    setTimeout(function(){ pymChild.sendHeight(); }, 20);
  }



  function get_state_rates() {


    // This is just setting max datestring, hmm
    prep_data_from_archive('dead_v_cases', '41000');

    Object.keys(coviddata).forEach(function(key) {
      
      var per_million_cases = 1000000 * coviddata[key][max_date_string]['c']/coviddata[key]['pop'];

      var per_million_deaths = 1000000 * coviddata[key][max_date_string]['d']/coviddata[key]['pop'];
      state_rate_dict[key] = per_million_cases;
      var is_bold = false;
      var name_formatted = coviddata[key]['name'];
      //name_formatted = name_formatted.replace('County', 'Cnty')

     
      var this_row = {
        name: name_formatted,
        pop: parseInt(coviddata[key]['pop']),
        cpm: per_million_cases,
        dpm: per_million_deaths,
        sortby: per_million_cases,
        isbold:is_bold
      }

      if (key == '41000') {
        this_row['name'] = "<b>Oregon Statewide</b>";
        this_row['sortby'] = -99999999;
        this_row['is_bold'] = true;
        regions_table.push(this_row);
        counties_table.push(this_row);
      }
      else if (key == '41420' || key=='38900') {
        regions_table.push(this_row);
      } else {
        counties_table.push(this_row);
      }
    });

    regions_table.sort((a, b) => (a.sortby < b.sortby) ? 1 : -1);
    counties_table.sort((a, b) => (a.sortby < b.sortby) ? 1 : -1);

  }

  // initial

  breaks = [400,600,800,1000];
  set_labels();
  get_state_rates();



function set_fill(featureid) {
    
    var rate = state_rate_dict[featureid];
    if (rate == 0) {
      return map_colors[0];
    }
    if (rate < breaks[0]) {
      return map_colors[1];
    }
    if (rate < breaks[1]) {
      return map_colors[2];
    }
    if (rate < breaks[2]) {
      return map_colors[3];
    }
    if (rate < breaks[3]) {
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
  padding: 7px;
}


.indented {
    text-indent: 10px;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}

.cshead {
   background-color: #f2f2f2;
}

.mdc-chip {

    font-family: Helvetica, Arial, 'Liberation Sans', FreeSans, sans-serif;
    
}
</style>


<div class="title">
<h3>Infection Rate by County</h3>
<p>As of April 23, 8 a.m.</p>
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
      <Points 
        projectionName={'geoMercator'}
        pointsData={points}
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
  <p class="byline">Scaled by cases per million</p>
</div>
</div>

<div class="data-container" style="margin-top:30px;">
<h2>Summary</h2>

<div style="margin:0px; padding:0px;">
    <Set chips={['Metro Areas', 'All Counties']} let:chip choice bind:selected={table_choice}>
      <Chip tabindex="0">{chip}</Chip>
    </Set>
  </div>


<p>Rates are expressed per <b>million</b> residents.</p>
{#if table_choice=='Metro Areas'}
  <table class="countysummary">
       <thead>
          <tr class="csrowheader">
            <th class="cshead">Area</th>
            <th class="cshead">Pop.</th>
            <th class="cshead">Case Rate</th>
          </tr>
        </thead>
    <tbody>
      {#each regions_table as region}
      <tr class="csrow">
        <td class="cscell">{@html region.name}</td>
        <td class="cscell">{format_number(region.pop)}</td>
        <td class="cscell">{format_rate(region.cpm)}</td>
      </tr>
      {/each}

    </tbody>
  </table>
  <p>
    The Portland area consists of Clackamas, Columbia, Multnomah, Washington and Yamhill counties. The Salem area consists of Marion and Polk counties.
      </p>
{:else}
  <table class="countysummary">
       <thead>
          <tr class="csrowheader">
            <th class="cshead">Area</th>
            <th class="cshead">Pop.</th>
            <th class="cshead">Case Rate</th>
          </tr>
        </thead>
    <tbody>
      {#each counties_table as region}
      <tr class="csrow">
        <td class="cscell">{@html region.name}</td>
        <td class="cscell">{format_number(region.pop)}</td>
        <td class="cscell">{format_rate(region.cpm)}</td>
      </tr>
      {/each}

    </tbody>
  </table>
{/if}
</div>

<div class="data-container" style="margin-top:20px; height: 80px;">
<p class="byline"><b>Sources:</b> Population estimates as of July, 1 2019, <a  target="_blank" href="https://www.pdx.edu/prc/population-reports-estimates">PSU</a>. Case and deaths are from the <a  target="_blank" href="https://govstatus.egov.com/OR-OHA-COVID-19">Oregon Health Authority</a>. 
</p>
</div>

