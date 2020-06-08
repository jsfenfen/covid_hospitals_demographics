<script>
  import { LayerCake, Svg, Html } from 'layercake';
  import { scaleOrdinal } from 'd3-scale';
   import { scaleBand } from 'd3-scale';

  import MapScale from './components/MapScale.svelte';
  import AxisXScaleBand from './components/AxisXScaleBand.svelte';
  import Points from './components/Points.svelte';


  import { feature } from 'topojson';
  import ORCounties from './data/orcounties.js';

  import { onMount } from 'svelte';

  import MapSvg from './components/MapSvg.svelte';
  const geojson = feature(ORCounties, ORCounties.objects.reprojection);



  import Tab, {Label as TabLabel} from '@smui/tab';
  import TabBar from '@smui/tab-bar';

  /* data */
  import coviddata from './data/coviddata.js'

  let active = 'New';
  let table_variable_name = 'New';
  let fill_mapping = {};

  let scaleword = "new cases";

  $: active, handleMapChange(active);

  let table_choice = 'Metro Areas';

  export const view_tabs = [
  { id: 'metro',  label: 'Metro Area' },
  { id: 'county',  label: 'County' },
  ];

  let activeTab;
  activeTab = view_tabs[0]; 

  $: activeTab, handleSelecta();

  onMount(() => {
    // Assumes that pymchild is defined on the page before here! 
    pymChild.sendHeight();
  });

  let breaks =  [] 

  let bar_chart_case_data = []
  let region_pop_data = {}

  let dead_v_cases;  // Only do this for the whole state. 
  let recent_date_text = 'June 7 at 12:01 a.m.'

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
    ]},
    {'name': 'Hermiston',
    'prominence':2,
    'points':[
        -119.2857, 
        45.8328
    ]},
    {'name': 'Coos Bay',
    'prominence':2,
    'points':[
        -124.2179, 
        43.3665
    ]},
    {'name': 'Madras',
    'prominence':2,
    'points':[
        -121.1295, 
        44.6335
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

  function set_labels() {

    labels = [
      {'label':'0'},
      {'label':'<' + breaks[0]},
      {'label':'<' + breaks[1]},
      {'label':'<' + breaks[2]},
      {'label':'<' + breaks[3]},
      {'label': breaks[3] + '+'}
    ]

    label_array = [];

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

  function format_number_type(region) {
    if (active == 'Deaths') {
      return format_number(region.deaths);
    }
    if (active == 'Cases') {
      return format_number(region.cases);
    }
    if (active == 'New') {
      return format_number(region.nc);
    }
  }

  


  function format_rate(num) {
    return parseFloat(num.toFixed(1));
  }

  function format_rate_type(region) {
    if (active == 'Deaths') {
      return format_rate(region.dpm);
    }
    if (active == 'Cases') {
      return format_rate(region.cpm);
    }
    if (active == 'New') {
      return format_rate(region.npm);
    }

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

  function handleSelecta() {
    if (activeTab.id == 'metro') {
      table_choice = 'Metro Areas';
    } else {
      table_choice = 'All Counties';
    }
    setTimeout(function(){ pymChild.sendHeight(); }, 20);
  }

  function get_state_rates() {

    // This is just setting max datestring, hmm
    prep_data_from_archive('dead_v_cases', '41000');

    var key_parts = max_date_string.split("_")

    var month = parseInt(key_parts[1]);
    var year = parseInt(key_parts[0]);
    var day = parseInt(key_parts[2]);

    // javascript has a month implementation bug
    var two_weeks_ago = new Date(year, month-1, day);

    two_weeks_ago.setDate( two_weeks_ago.getDate() - 14 );

    var this_month = String(two_weeks_ago.getMonth() + 1); // js months!
    this_month = this_month.padStart(2,'0');
    var this_year = two_weeks_ago.getFullYear();
    var this_day = String(two_weeks_ago.getDate()).padStart(2,'0');

    var two_weeks_ago_datestring = this_year + "_" + this_month + "_" + this_day;

    Object.keys(coviddata).forEach(function(key) {
      
      var cases_in_last_two_weeks = coviddata[key][max_date_string]['c'] - coviddata[key][two_weeks_ago_datestring]['c']

      var per_10K_new_cases = 10000 * cases_in_last_two_weeks / coviddata[key]['pop']

      var per_10K_cases = 10000 * coviddata[key][max_date_string]['c']/coviddata[key]['pop'];

      var per_10K_deaths = 10000 * coviddata[key][max_date_string]['d']/coviddata[key]['pop'];
      var is_bold = false;
      var name_formatted = coviddata[key]['name'];
     
      var this_row = {
        name: name_formatted,
        pop: parseInt(coviddata[key]['pop']),
        nc:parseInt(cases_in_last_two_weeks),
        cases:parseInt(coviddata[key][max_date_string]['c']),
        deaths:parseInt(coviddata[key][max_date_string]['d']),
        cpm: per_10K_cases,
        dpm: per_10K_deaths,
        npm: per_10K_new_cases,
        sortby: per_10K_cases,
        isbold:is_bold
      }

      state_rate_dict[key] = {
        cpm: per_10K_cases,
        dpm: per_10K_deaths,
        npm: per_10K_new_cases
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

    // Create a synthetic "rest of state"
    var ros_pop = parseInt(coviddata['41000']['pop']) - parseInt(coviddata['38900']['pop']) - parseInt(coviddata['41420']['pop'])

    var ros_cases_two_weeks_ago  = parseInt(coviddata['41000'][two_weeks_ago_datestring]['c']) - ( parseInt(coviddata['41420'][two_weeks_ago_datestring]['c']) + parseInt(coviddata['38900'][two_weeks_ago_datestring]['c']) )
    var ros_cases = parseInt(coviddata['41000'][max_date_string]['c']) - ( parseInt(coviddata['41420'][max_date_string]['c']) + parseInt(coviddata['38900'][max_date_string]['c']) )
    var ros_nc = ros_cases - ros_cases_two_weeks_ago;
    var ros_deaths = parseInt(coviddata['41000'][max_date_string]['d']) - ( parseInt(coviddata['41420'][max_date_string]['d']) + parseInt(coviddata['38900'][max_date_string]['d']) )

    var ros_pop = parseInt(coviddata['41000']['pop']) - parseInt(coviddata['38900']['pop']) - parseInt(coviddata['41420']['pop'])

    var ros_per_10K_new_cases = 10000 * ros_nc / ros_pop;
    var ros_per_10K_cases = 10000 * ros_cases/ros_pop;
    var ros_per_10K_deaths = 10000 * ros_deaths/ros_pop;

    var rest_of_state_row = {
      name: "Rest of state",
      pop: ros_pop,
      nc:ros_nc,
      cases:ros_cases,
      deaths:ros_deaths,
      cpm: ros_per_10K_cases,
      dpm: ros_per_10K_deaths,
      npm: ros_per_10K_new_cases,
    }
    regions_table.push(rest_of_state_row);

  }


  function set_breaks(these_breaks, display_type) {
    breaks = these_breaks;
    set_labels();
    make_fill_mapping(display_type);
    fill_mapping = fill_mapping;
    geojson = geojson;
  }

  get_state_rates();



  function set_fill(rate) {
    
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

  function make_fill_mapping(lookupkey) {
    // iey should be cpm, dpm or npm for cases, deaths, new cases
    fill_mapping = {};

    Object.keys(coviddata).forEach(function(key) {
      var this_rate = state_rate_dict[key][lookupkey];
      var this_fill = set_fill(this_rate);
      fill_mapping[key] = this_fill;
    });
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


  function handleMapChange(maptype) {

    if (maptype == 'Deaths') {
      set_breaks([0.25,0.5,0.75,1], 'dpm');
      table_variable_name = 'Deaths';
      regions_table.sort((a, b) => (a.dpm < b.dpm) ? 1 : -1);
      counties_table.sort((a, b) => (a.dpm < b.dpm) ? 1 : -1);
      scaleword = "deaths";
    }
    if (maptype == 'Cases') {
      set_breaks([5,10,15,20], 'cpm');
      table_variable_name = 'Cases';
      regions_table.sort((a, b) => (a.cpm < b.cpm) ? 1 : -1);
      counties_table.sort((a, b) => (a.cpm < b.cpm) ? 1 : -1);
      scaleword = "cases";

    }
    if (maptype == 'New') {
      set_breaks([2.5,5,7.5,10], 'npm');
      table_variable_name = 'New Cases';
      regions_table.sort((a, b) => (a.npm < b.npm) ? 1 : -1);
      counties_table.sort((a, b) => (a.npm < b.npm) ? 1 : -1);
      scaleword = "new cases";
    }
    // We may have to do these assignments to trigger svelte updates? 
    regions_table = regions_table;
    counties_table = counties_table;
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
  padding: 3px;
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
<h3>Virus Spread by County</h3>
<p>As of { recent_date_text} New cases are confirmed and "presumptive" positives reported within the last two weeks.</p>
</div>


<div class="title">
<div style="margin-bottom: 20px;">
    <TabBar tabs={['New', 'Cases', 'Deaths']} let:tab bind:active>
      <Tab {tab} minWidth>
        <TabLabel>{tab}</TabLabel>
      </Tab>
    </TabBar>
  </div>
</div>

<div class="chart-container">
  <LayerCake
    data={geojson}
  >
    <Svg>
      <MapSvg
        projectionName={'geoMercator'}
        fill_mapping={fill_mapping}
        features={geojson.features}
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
  <div style="margin-left:20px;">
  <p class="byline"><b>Note:</b> Scaled by {scaleword} per 10,000.</p>
</div>
</div>

<div class="data-container" style="margin-top:30px;">
<h2>Summary by area</h2>

<div class="title">
  <div style="margin:0px; padding:0px;">
    <TabBar tabs={view_tabs} let:tab minWidth bind:active={activeTab}>
      <Tab {tab}>
        <TabLabel>{tab.label}</TabLabel>
      </Tab>
    </TabBar>
  </div>
</div>

<p>Rates are expressed per <b>10,000</b> residents. New cases are the number announced in the last two weeks. Includes state-designated "presumptive" cases, in which patients show COVID-like symptoms and have been in "close contact with a confirmed case".</p>
{#if table_choice=='Metro Areas'}
  <table class="countysummary">
       <thead>
          <tr class="csrowheader">
            <th class="cshead">Area</th>
            <th class="cshead">Pop.</th>
            <th class="cshead">{ table_variable_name }</th>
            <th class="cshead">Rate</th>
          </tr>
        </thead>
    <tbody>
      {#each regions_table as region}
      <tr class="csrow">
        <td class="cscell">{@html region.name}</td>
        <td class="cscell">{format_number(region.pop)}</td>
        <td class="cscell">{format_number_type(region)}</td>
        <td class="cscell">{format_rate_type(region)}</td>
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
            <th class="cshead">{ table_variable_name }</th>
            <th class="cshead">Rate</th>
          </tr>
        </thead>
    <tbody>
      {#each counties_table as region}
      <tr class="csrow">
        <td class="cscell">{@html region.name}</td>
        <td class="cscell">{format_number(region.pop)}</td>
        <td class="cscell">{format_number_type(region)}</td>
        <td class="cscell">{format_rate_type(region)}</td>
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



