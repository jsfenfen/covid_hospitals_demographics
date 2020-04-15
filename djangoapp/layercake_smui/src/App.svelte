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


  import { feature } from 'topojson';
  //import usStates from './data/us-states.topojson.js';
  import ORCounties from './data/orcounties.js';


  import MapSvg from './components/MapSvg.svelte';

  const geojson = feature(ORCounties, ORCounties.objects.reprojection);


  import { onMount } from 'svelte';

  /* data */
  import data from './data/testdata2.js';
  //import multidata from './data/testdata.js';
  import coviddata from './data/coviddata.js'

  /* svelte smui */

  
  import {MDCSelect} from '@material/select';
  import Select, { Option } from "@smui/select";

  import DataTable, {Head, Body, Row, Cell} from '@smui/data-table';

  //import Select, {Option} from '@smui/select';

  //import Select from 'svelte-select';

  let bar_chart_case_data = []
  let region_pop_data = {}

  const items = [
    {value: '41000', label: 'Oregon statewide', group: 'State'},
    {value: '38900', label: 'Portland', group: 'Metro Areas'},
    {value: '41420', label: 'Salem', group: 'Metro Areas'},
    //{value: '41001', label: 'Baker County', group: 'Counties'},
    {value: '41003', label: 'Benton County', group: 'Counties'},
    {value: '41005', label: 'Clackamas County', group: 'Counties'},
    {value: '41007', label: 'Clatsop County', group: 'Counties'},
    {value: '41009', label: 'Columbia County', group: 'Counties'},
    //{value: '41011', label: 'Coos County', group: 'Counties'},
    {value: '41013', label: 'Crook County', group: 'Counties'},
    {value: '41015', label: 'Curry County', group: 'Counties'},
    {value: '41017', label: 'Deschutes County', group: 'Counties'},
    {value: '41019', label: 'Douglas County', group: 'Counties'},
    //{value: '41021', label: 'Gilliam County', group: 'Counties'},
    {value: '41023', label: 'Grant County', group: 'Counties'},
    //{value: '41025', label: 'Harney County', group: 'Counties'},
    {value: '41027', label: 'Hood River County', group: 'Counties'},
    {value: '41029', label: 'Jackson County', group: 'Counties'},
    //{value: '41031', label: 'Jefferson County', group: 'Counties'},
    {value: '41033', label: 'Josephine County', group: 'Counties'},
    {value: '41035', label: 'Klamath County', group: 'Counties'},
    //{value: '41037', label: 'Lake County', group: 'Counties'},
    {value: '41039', label: 'Lane County', group: 'Counties'},
    {value: '41041', label: 'Lincoln County', group: 'Counties'},
    {value: '41043', label: 'Linn County', group: 'Counties'},
    {value: '41045', label: 'Malheur County', group: 'Counties'},
    {value: '41047', label: 'Marion County', group: 'Counties'},
    {value: '41049', label: 'Morrow County', group: 'Counties'},
    {value: '41051', label: 'Multnomah County', group: 'Counties'},
    {value: '41053', label: 'Polk County', group: 'Counties'},
    {value: '41055', label: 'Sherman County', group: 'Counties'},
    {value: '41057', label: 'Tillamook County', group: 'Counties'},
    {value: '41059', label: 'Umatilla County', group: 'Counties'},
    {value: '41061', label: 'Union County', group: 'Counties'},
    {value: '41063', label: 'Wallowa County', group: 'Counties'},
    {value: '41065', label: 'Wasco County', group: 'Counties'},
    {value: '41067', label: 'Washington County', group: 'Counties'},
    //{value: '41069', label: 'Wheeler County', group: 'Counties'},
    {value: '41071', label: 'Yamhill County', group: 'Counties'}
  ];


  // the selected item is temporarily removed from the list when selected
  // make a lookup for it. 
  var itemlookup = {};
  items.forEach(function (item, index) {
    itemlookup[item.value] = item.label;
  });


  let dialog;
  let submitdialog;

  let explainer_text = '';
  let region_text = '';


  let dialogue_message = '';
  let dialogue_title = '';

  let cases;
  let deaths;
  let new_cases;
  let tests;
  let dead_v_cases;  // Only do this for the whole state. 

  let cases_long;
  let cases_series;
  let cases_domain;
  
  let dead_v_cases_long
  let dead_v_cases_series;
  let dead_v_cases_domain;

  let deaths_long;
  let deaths_series;
  let deaths_domain;

  let new_cases_long;
  let new_cases_series;
  let new_cases_domain;


  let tests_long;
  let tests_series;
  let tests_domain;



  let colorScale;
  let cases_colorScale;
  let deaths_colorScale;
  let new_cases_colorScale;
  let tests_colorScale;
  let dead_v_cases_colorScale;

  let isClearable = false;

  let state_rate_dict = {};

  let max_date_string;

  const map_colors = ['#ffdecc', '#ffc09c', '#ffa06b', '#ff7a33'];


  let selectedFIPS = '41000';
  let regionDisplay = 'Oregon statewide';

  // Hmm... https://stackoverflow.com/questions/56983938/in-svelte-how-to-console-logyes-when-a-variable-changed
  $: selectedFIPS, handleSelect(selectedFIPS);

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

  function handleSelect(thisfips) {
    
    if (!thisfips) {
      console.log("fips undefined, skipping");
      return null;

    }
    regionDisplay = itemlookup[thisfips];

    set_data(thisfips);


    if (thisfips == '38900') {
      explainer_text = 'The Portland area consists of Clackamas, Columbia, Multnomah, Washington and Yamhill counties.'
    } else if (thisfips == '41420') {
      explainer_text = 'The Salem area consists of Marion and Polk counties.'
    } else {
      explainer_text = '';
    }



    region_text = regionDisplay + " has a total population of " + format_number(coviddata[thisfips]['pop']) + " and " + format_number(100*coviddata[thisfips]['fraction_65_over'])  + "% are over 65. As of " + format_date_string(max_date_string) + " a total of " + format_number(coviddata[thisfips][max_date_string]['c']) + " confirmed cases and " + format_number(coviddata[thisfips][max_date_string]['d']) + " deaths have been reported to the state health department. The actual number of cases is significantly higher."
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
    '#ffe4b8',
    '#ffb3c0',
    '#ff7ac7',
    '#ff00cc'
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
    console.log('dead_v_cases')
    console.log(dead_v_cases)
    dead_v_cases_long = get_long_data(dead_v_cases);
    dead_v_cases_series = get_series_names(dead_v_cases);
    dead_v_cases_domain = get_domain(dead_v_cases_long,true);
    console.log('dead_v_cases_domain')
    console.log(dead_v_cases_domain)

    dead_v_cases_colorScale = scaleOrdinal()
      .domain(cases_series)
      .range(seriesColors);


    var portland_cases = coviddata['38900'][max_date_string]['c'];
    var salem_cases = coviddata['41420'][max_date_string]['c'];
    var ros_cases = coviddata['41000'][max_date_string]['c'] - portland_cases - salem_cases;
    console.log(bar_chart_case_data);

    bar_chart_case_data.push({'name':'Rest of state','cases':ros_cases})
    bar_chart_case_data.push({'name':'Salem Area','cases':salem_cases})
    bar_chart_case_data.push({'name':'Portland Area','cases':portland_cases})

    console.log(bar_chart_case_data);

    region_pop_data['metro_pop'] = coviddata['38900']['pop'] + coviddata['41420']['pop'];
    region_pop_data['rest_pop'] = coviddata['41000']['pop'] - region_pop_data['metro_pop'];



  
  }

  function set_data(fips){
    cases = prep_data_from_archive('cases', fips);
    deaths = prep_data_from_archive('deaths', fips);
    new_cases = prep_data_from_archive('new_cases', fips);
    tests = prep_data_from_archive('tests', fips);

    cases_long = get_long_data(cases);
    cases_series = get_series_names(cases);
    cases_domain = get_domain(cases_long,false);

    tests_long = get_long_data(tests);
    tests_series = get_series_names(tests);
    tests_domain = get_domain(tests_long,false);

    deaths_long = get_long_data(deaths);
    deaths_series = get_series_names(deaths);
    deaths_domain = get_domain(deaths_long,false);

    new_cases_long = get_long_data(new_cases);
    new_cases_series = get_series_names(new_cases);
    new_cases_domain = get_domain(new_cases_long,false);

    cases_colorScale = scaleOrdinal()
      .domain(cases_series)
      .range(seriesColors);

    new_cases_colorScale = scaleOrdinal()
      .domain(new_cases_series)
      .range(seriesColors);

    deaths_colorScale = scaleOrdinal()
      .domain(deaths)
      .range(seriesColors);
    

    tests_colorScale = scaleOrdinal()
      .domain(deaths)
      .range(seriesColors);
    }

  set_data('41000');
  set_sitewide_charts();

  function get_state_rates() {
    Object.keys(coviddata).forEach(function(key) {
      
      var per_million_cases = 1000000 * coviddata[key][max_date_string]['c']/coviddata[key]['pop'];

      var per_million_deaths = 1000000 * coviddata[key][max_date_string]['d']/coviddata[key]['pop'];
      state_rate_dict[key] = per_million_cases;
      var is_bold = false;
      var name_formatted = coviddata[key]['name'];

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
    if (rate > 500) {
      return map_colors[3];
    }
    if (rate > 400) {
      return map_colors[2];
    }
    if (rate > 300) {
      return map_colors[1];
    }
    if (rate == 0) {
      return '#ffffff';
    }
    return map_colors[0];
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

/*
  function show_help(title, message) {
      dialogue_title = "About";
      dialogue_message = 'Some text';
      submitdialog.open();
  }

*/

  
</script>

<style>
  .chart-container {
    width: 100%;
    max-width: 500px;
    height: 300px;
  }

    .chart-container-short {
    width: 100%;
    max-width: 500px;
    height: 150px;
  }

  .data-container {
    width: 100%;
    max-width: 500px;
  }
  .title {
  	margin-top: 20px;
    width: 100%;
    max-width: 500px;
  }
  .selectionholder {
    width: 100%;
  }
  .source {
    font-size: 12px;
  }

  @import url(https://unpkg.com/@smui/select@latest/bare.css);

</style>


<div class="title">
<div class="selectionholder">
<Select variant="outlined" enhanced bind:value={selectedFIPS} label="Select a region" class="demo-select-width" menu$class="demo-select-width">
          <Option value=""></Option>
          {#each items as item}
            <Option value={item.value} selected={selectedFIPS === item.value}>{item.label}</Option>
          {/each}
        </Select>
</div>


<h2>Total cases, {regionDisplay}</h2>

<p>{explainer_text}</p>
<p>{region_text}</p>
</div>

<div class="chart-container">
  
  <LayerCake
    padding={{ top: 27, right: 10, bottom: 20, left: 40 }}
    x='month'
    y='value'
    flatData={flatten(cases_long)}
    yDomain={cases_domain}
    data={cases_long}
  >
    <Svg>
      <AxisX
        gridlines={false}
        ticks={cases.map(d => d[xKey])}
        formatTick={formatTickX}
        snapTicks={true}
      />
      <AxisY
        formatTick={formatTickY}
      />

      <MultiLine
        colorScale={cases_colorScale}
      />
    </Svg>

    <Html>
      <Labels/>
      <Tooltip
        dataset={ cases }
      />
    </Html>
  </LayerCake>
</div>

<div class="title">
<h2>Total deaths, {regionDisplay}</h2>
</div>

<div class="chart-container">
  
  <LayerCake
    padding={{ top: 27, right: 10, bottom: 20, left: 40 }}
    x='month'
    y='value'
    flatData={flatten(deaths_long)}
    yDomain={deaths_domain}
    data={deaths_long}
  >
    <Svg>
      <AxisX
        gridlines={false}
        ticks={deaths.map(d => d[xKey])}
        formatTick={formatTickX}
        snapTicks={true}
      />
      <AxisY
        formatTick={formatTickY}
      />

      <MultiLine
        colorScale={deaths_colorScale}
      />
    </Svg>

    <Html>
      <Labels/>
      <Tooltip
        dataset={ deaths }
      />
    </Html>
  </LayerCake>
</div>

<div class="title">
<h2>Daily new cases, {regionDisplay}</h2>
</div>

<div class="chart-container">
  
  <LayerCake
    padding={{ top: 27, right: 10, bottom: 20, left: 40 }}
    x='month'
    y='value'
    yDomain={new_cases_domain}
    flatData={flatten(new_cases_long)}
    data={new_cases_long}
  >
    <Svg>
      <AxisX
        gridlines={false}
        ticks={new_cases.map(d => d[xKey])}
        formatTick={formatTickX}
        snapTicks={true}
      />
      <AxisY
        formatTick={formatTickY}
      />

      <MultiLine
        colorScale={new_cases_colorScale}
      />
    </Svg>

    <Html>
      <Labels/>
      <Tooltip
        dataset={ new_cases }
      />
    </Html>
  </LayerCake>
</div>



<div class="title">
<h2>Daily test results, {regionDisplay}</h2>
</div>

<div class="chart-container">
  
  <LayerCake
    padding={{ top: 27, right: 10, bottom: 20, left: 40 }}
    x='month'
    y='value'
    yDomain={tests_domain}
    flatData={flatten(tests_long)}
    data={tests_long}
  >
    <Svg>
      <AxisX
        gridlines={false}
        ticks={new_cases.map(d => d[xKey])}
        formatTick={formatTickX}
        snapTicks={true}
      />
      <AxisY
        formatTick={formatTickY}
      />

      <MultiLine
        colorScale={tests_colorScale}
      />
    </Svg>

    <Html>
      <Labels/>
      <MultiTooltip
        dataset={ tests }
      />
    </Html>
  </LayerCake>
</div>

<div class="title">
  <h1>State statistics</h1>
</div>

<div class="title">
  <h2>Cases by region</h2>
</div>
  <div class="chart-container-short">
  <LayerCake
    padding={{ top: 0, bottom: 20, left: 85 }}
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
      <Bar/>
    </Svg>
  </LayerCake>
</div>

<div class="title">
<h2>Total deaths and cases, log scale</h2>
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
        ticks={data.map(d => d[xKey])}
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

<div class="title">
<h2>Counties, by cases per capita</h2>
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

<div class="data-container">
<h2>County summary</h2>

<DataTable class="mdc-data-table__table mdc-layout-grid__cell--span-12">
       <Head >
          <Row class="mdc-layout-grid__cell--span-12">
            <Cell>Area</Cell>
            <Cell>Pop.</Cell>
            <Cell>Cases/million</Cell>
            <Cell>Deaths/million</Cell>

          </Row>
        </Head>
    <Body>
      {#each results_for_table as region}
      <Row class="mdc-layout-grid__cell--span-12">
        <Cell>{@html region.name}</Cell>
        <Cell>{format_number(region.pop)}</Cell>
        <Cell>{format_rate(region.cpm)}</Cell>
        <Cell>{format_rate(region.dpm)}</Cell>
      </Row>
      {/each}

    </Body>
  </DataTable>

</div>

<div class="data-container">
<p class="source"><b>Sources:</b> Population estimates as of July, 1 2019, <a href="https://www.pdx.edu/prc/population-reports-estimates">PSU</a>. Case and deaths are from the <a href="https://govstatus.egov.com/OR-OHA-COVID-19">Oregon Health Authority</a>. 
<br><b>Notes:</b> Dates of "new cases" reflect the day they were announced, not the day the individual became symptomatic. The latter information, which is more useful for epidemiology, is not released by the state.</p>
</div>


