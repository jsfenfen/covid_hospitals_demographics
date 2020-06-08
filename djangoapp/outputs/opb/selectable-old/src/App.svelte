<script>
  import { LayerCake, Svg, Html } from 'layercake';
  import { scaleOrdinal } from 'd3-scale';
   import { scaleLog, scaleBand } from 'd3-scale';

  import MultiLine from './components/MultiLine.svelte';
  import BarTrend from './components/BarTrend.svelte';
  import DotTrend from './components/DotTrend.svelte';

  import ReStackedBar from './components/ReStackedBar.svelte';

  import BarTrendTooltip from './components/BarTrendTooltip.svelte';
  import DotTrendTooltip from './components/DotTrendTooltip.svelte';
  import ReStackedBarTooltip from './components/ReStackedBarTooltip.svelte';


  import AxisX from './components/AxisX.svelte';
  import AxisY from './components/AxisY.svelte';
  import AxisYLog from './components/AxisYLog.svelte';
  import Labels from './components/Labels.svelte';

  import Tooltip from './components/Tooltip.svelte';
  import MultiTooltip from './components/MultiTooltip.svelte';
  import QuadTree from './components/QuadTree.svelte';
  import AxisYScaleBand from './components/AxisYScaleBand.svelte';
  import Bar from './components/Bar.svelte';

  import Switch from '@smui/switch';
  import FormField from '@smui/form-field';


  import { onMount } from 'svelte';

  /* data */
  import coviddata from './data/coviddata.js'

  /* svelte smui */


  
  import {MDCSelect} from '@material/select';
  import Select, { Option } from "@smui/select";

  const items = [
    {value: '41000', label: 'Oregon', group: 'State'},
    {value: '38900', label: 'Portland', group: 'Metro Areas'},
    {value: '41420', label: 'Salem', group: 'Metro Areas'},
    //{value: '41001', label: 'Baker County', group: 'Counties'},
    {value: '41003', label: 'Benton County', group: 'Counties'},
    {value: '41005', label: 'Clackamas County', group: 'Counties'},
    {value: '41007', label: 'Clatsop County', group: 'Counties'},
    {value: '41009', label: 'Columbia County', group: 'Counties'},
    {value: '41011', label: 'Coos County', group: 'Counties'},
    {value: '41013', label: 'Crook County', group: 'Counties'},
    {value: '41015', label: 'Curry County', group: 'Counties'},
    {value: '41017', label: 'Deschutes County', group: 'Counties'},
    {value: '41019', label: 'Douglas County', group: 'Counties'},
    //{value: '41021', label: 'Gilliam County', group: 'Counties'},
    {value: '41023', label: 'Grant County', group: 'Counties'},
    {value: '41025', label: 'Harney County', group: 'Counties'},
    {value: '41027', label: 'Hood River County', group: 'Counties'},
    {value: '41029', label: 'Jackson County', group: 'Counties'},
    {value: '41031', label: 'Jefferson County', group: 'Counties'},
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

  let show_nc = true;
  let show_d = true;
  let show_c = true;
  let show_t = true;

  let dialogue_message = '';
  let dialogue_title = '';

  let cases;
  let deaths;
  let new_cases;
  let new_deaths;
  let tests;
  let positivity;
  let dead_v_cases;  // Only do this for the whole state. 


  let has_deaths = false;

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

  let new_deaths_long;
  let new_deaths_series;
  let new_deaths_domain;

  let tests_long;
  let tests_series;
  let tests_domain;

  let positivity_long;
  let positivity_series;
  let positivity_domain;

  let colorScale;
  let cases_colorScale;
  let deaths_colorScale;
  let new_deaths_colorScale;

  let new_cases_colorScale;
  let tests_colorScale;
  let positivity_colorScale;

  let dead_v_cases_colorScale;

  let isClearable = false;

  let state_rate_dict = {};

  let max_date_string;

  const map_colors = ['#ffdecc', '#ffc09c', '#ffa06b', '#ff7a33'];

  let recent_date_text = 'May 11 at 8 a.m.'

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

    var case_plural = (coviddata[thisfips][max_date_string]['n_c'] != 1 ? 's':'');
    var death_plural = (coviddata[thisfips][max_date_string]['n_d'] != 1 ? 's':'');


    region_text = regionDisplay + " reported a total of " + format_number(coviddata[thisfips][max_date_string]['c']) + " confirmed cases and " + format_number(coviddata[thisfips][max_date_string]['d']) + " deaths as of " + format_date_string(max_date_string) + ", including <b>" + coviddata[thisfips][max_date_string]['n_c'] + "</b> new case" + case_plural + " and <b>" + coviddata[thisfips][max_date_string]['n_d'] + "</b> new death" + death_plural + "."; 


    has_deaths = coviddata[thisfips][max_date_string]['d'] > 0;
    

    // Assumes that pymchild is defined on the page before here! 
    setTimeout(function(){ pymChild.sendHeight(); }, 20);
    //console.log("height sent");
  }

  function prep_data_from_archive(data_type, fips) {

    var data_for_this_fips = [];
    var this_jurisdiction = coviddata[fips];
    var day_count = 0;

    var new_case_ma = [-1,-1,-1,-1,-1,-1,-1];
    var new_death_ma = [-1,-1,-1,-1,-1,-1,-1];

    var positivity_ma = [-1,-1,-1,-1,-1,-1,-1];

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
          if (day_count > 1)  {
          
            var new_case_count = this_jurisdiction[key]['n_c'];
            if (new_case_count < 0) {
              new_case_count = 0;
            }

            var this_average;
            var sum=0;
            var valid_values = 0;
            // futzing with this, cleanup when we know how it should work
            new_case_ma.push(new_case_count);
            new_case_ma.shift();

            new_case_ma.forEach(val => { 
              if (val!=-1) {
                valid_values++;
                sum += val;
              }
            });
            this_average = sum / valid_values;
          
          // we don't have 'new' cases on day 1

            data_for_this_fips.push({'month':this_date, 'New Cases':new_case_count, 'Trend':this_average});
          }
        }
        if (data_type == 'deaths') {
          var death_count = this_jurisdiction[key]['d'];
          data_for_this_fips.push({'month':this_date, 'Deaths':death_count});
        }

        if (data_type == 'tests') {
          if (day_count > 2)  {
            data_for_this_fips.push({'month':this_date, 'Negatives':this_jurisdiction[key]['n_n'], 'Positives':this_jurisdiction[key]['n_c'], 'Total':this_jurisdiction[key]['n_n']+this_jurisdiction[key]['n_c']});
          }
        }

        if (data_type == 'positivity') {
          if (day_count > 2)  {
            var total_tests = this_jurisdiction[key]['n_c'] + this_jurisdiction[key]['n_n'];
            var positive_rate = 0;
            if (total_tests > 0 ) {
              positive_rate = 100*this_jurisdiction[key]['n_c']/total_tests;
            }
            if (positive_rate < 0) {
              positive_rate = 0;
            }


            // futzing with this, cleanup when we know how it should work
            if (day_count == 34 || day_count == 35) {
              positivity_ma.push(-1);
            } else {
              positivity_ma.push(positive_rate);
            }
            positivity_ma.shift();

            var this_average;
            var sum=0;
            var valid_values = 0;
            positivity_ma.forEach(val => { 
              if (val!=-1) {
                valid_values++;
                sum += val;
              }
            });
            this_average = sum / valid_values;


            if (day_count != 34 && day_count != 35) {
              data_for_this_fips.push({'month':this_date, 'Rate':parseFloat(positive_rate.toFixed(1)), 'Trend':this_average});
            }
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

            var this_average;
            var sum=0;
            var valid_values = 0;
            // futzing with this, cleanup when we know how it should work
            new_death_ma.push(new_death_count);

            new_death_ma.shift();

            new_death_ma.forEach(val => { 
              if (val!=-1) {
                valid_values++;
                sum += val;
              }
            });
            this_average = sum / valid_values;


            data_for_this_fips.push({'month':this_date, 'New Deaths':new_death_count, 'Trend':this_average});
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
  ];


  var seriesColors2 = [
    '#6d6d00',
    '#b2bc00',
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

  // Todo: write this more declaratively
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

  

  function set_data(fips){
    cases = prep_data_from_archive('cases', fips);
    deaths = prep_data_from_archive('deaths', fips);
    new_cases = prep_data_from_archive('new_cases', fips);
    new_deaths = prep_data_from_archive('new_deaths', fips);
    tests = prep_data_from_archive('tests', fips);
    positivity = prep_data_from_archive('positivity', fips);

    cases_long = get_long_data(cases);
    cases_series = get_series_names(cases);
    cases_domain = get_domain(cases_long,false);

    tests_long = get_long_data(tests);
    tests_series = get_series_names(tests);
    tests_domain = get_domain(tests_long,false);

    positivity_long = get_long_data(positivity);
    positivity_series = get_series_names(positivity);
    positivity_domain = get_domain(positivity_long,false);
    console.log("Got positivity domain " + positivity_domain + " from ");
    console.log(positivity_long);

    deaths_long = get_long_data(deaths);
    deaths_series = get_series_names(deaths);
    deaths_domain = get_domain(deaths_long,false);

    new_deaths_long = get_long_data(new_deaths);
    new_deaths_series = get_series_names(new_deaths);
    new_deaths_domain = get_domain(new_deaths_long,false);

    console.log("New deaths");
    console.log(new_deaths);


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
    
    new_deaths_colorScale = scaleOrdinal()
      .domain(new_deaths)
      .range(seriesColors2);

    tests_colorScale = scaleOrdinal()
      .domain(tests)
      .range(seriesColors);

    positivity_colorScale = scaleOrdinal()
      .domain(positivity)
      .range(seriesColors);
    }

  set_data('41000');

  function formatTickX (d) {
    const date = new Date(d);
    var day = date.getDate();
    var dayofweek = date.getDay()
    if (dayofweek==0 ) {
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

  onMount(() => {
    // Assumes that pymchild is defined on the page before here! 
    pymChild.sendHeight();
  });

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
    font-family: Georgia, Times, 'Times New Roman', serif;
    color:  #333333;
    font-size: 18px;
    line-height: 1.5em;
    margin-bottom: 20px;
  }
  .selectionholder {
    width: 100%;
  }
  .source {
    font-size: 12px;
  }

  .switch-container {
    display:inline;
    margin-left: 10px;
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
</div>

<div class="title">

<h3>New Confirmed Cases, {regionDisplay}</h3>
<p>{explainer_text}</p>
<p>{@html region_text}</p>

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

      <BarTrend
        colorScale={new_cases_colorScale}
      />
    </Svg>

    <Html>
      <BarTrendTooltip

        dataset={ new_cases }
      />
    </Html>
  </LayerCake>
</div>
<div class="title">

<b>What this Chart Means:</b><br>
<p> One key question is how quickly the virus is spreading. This chart shows lab-confirmed cases and state-designated "presumptive" cases, in which patients show COVID-like symptoms and have been in "close contact with a confirmed case". The actual number of cases is likely considerably higher. Many cases are asymptomatic. Until there's widely available antibody testing, many who catch the virus will never know they had it. </p>
<p>The date shown is the day that the state announced the case, not the day that the person caught the virus. It may take several days to a week for results to become available, so this chart lags behind reality. People who catch the virus often recover within 21 days of becoming symptomatic, although less severe cases may pass quicker.</p>


<p><b>Notes:</b> The black line is a 7-day moving average. </p>
</div>


{#if has_deaths }

<div class="title">

<h3>New Deaths, {regionDisplay}</h3>
</div>

<div class="chart-container">
  
  <LayerCake
    padding={{ top: 27, right: 10, bottom: 20, left: 40 }}
    x='month'
    y='value'
    yDomain={new_deaths_domain}
    flatData={flatten(new_deaths_long)}
    data={new_deaths_long}
  >
    <Svg>
      <AxisX
        gridlines={false}
        ticks={new_deaths.map(d => d[xKey])}
        formatTick={formatTickX}
        snapTicks={true}
      />
      <AxisY
        formatTick={formatTickY}
      />

      <BarTrend
        colorScale={new_cases_colorScale}
        fill="#6d6d00"
      />
    </Svg>

    <Html>
      <BarTrendTooltip

        dataset={ new_deaths }
      />
    </Html>
  </LayerCake>
</div>
<div class="title">

<b>What this Chart Means:</b><br>
<p>This chart shows known deaths due to COVID-19. It is an undercount. In other areas total deaths have been adjusted upwards later to include deaths at home, in homeless camps, and where testing was not immediately available.</p>


<p><b>Notes:</b> The black line is a 7-day moving average. </p>
</div>


<div class="title">
<h3>Total Cases, {regionDisplay}</h3>
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
<p><b>What this Chart Means:</b> <br>When transmission of the virus stops, this chart will flatten out. Early indications are that social distancing has slowed the spread of the virus. This chart shows only laboratory-confirmed cases, so the total number of actual cases is significantly higher.</p>
</div>



<div class="title">
<h3>Total Deaths, {regionDisplay}</h3>
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
<p><b>What this Chart Means:</b><br> Our understanding of the virus is that people often become symptomatic 5-7 days after exposure. While the vast number survive, some <a href="https://www.thelancet.com/action/showPdf?pii=S0140-6736%2820%2930566-3" target="_blank">published reports</a> estimate the time from symptom onset until death to be 19 days, although this number varies. The effects of social distancing should be evident in deaths reported within about 25 days.</p>
</div>

{/if }


<div class="title">
<h3>Daily Test Results, {regionDisplay}</h3>
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

      <ReStackedBar
        colorScale={tests_colorScale}
      />
    </Svg>

    <Html>
      <ReStackedBarTooltip
        dataset={ tests }
      />
    </Html>
  </LayerCake>
</div>

 <div class="title">
<p><b>What this Chart Means</b>

<br>Widely available testing is one of the key requirements to ending social distancing, although epidemiologists argue it's <a  target="_blank" href="https://www.statnews.com/2020/03/24/we-need-smart-coronavirus-testing-not-just-more-testing/">not just the number of tests that matter</a>. One team at Harvard suggests reopening states would require <a  target="_blank" href="https://www.nytimes.com/interactive/2020/04/17/us/coronavirus-testing-states.html">152 tests per 100,000 residents</a>, which translates into more than 6,400 tests in Oregon daily.
</p>
<p><b>Notes:</b> On April 22 state authorities did not provide a negative test count, noting instead that negative "results are pending due to a technical issue with the test reporting database".</p>
</div>


<div class="title">
<h3>Test Positivity Rate, {regionDisplay}</h3>
</div>

<div class="chart-container">
  
  <LayerCake
    padding={{ top: 27, right: 10, bottom: 20, left: 40 }}
    x='month'
    y='value'
    flatData={flatten(positivity_long)}
    yDomain={positivity_domain}
    data={positivity_long}
  >
    <Svg>
      <AxisX
        gridlines={false}
        ticks={positivity.map(d => d[xKey])}
        formatTick={formatTickX}
        snapTicks={true}
      />
      <AxisY
        formatTick={formatTickY}
      />

      <DotTrend
        colorScale={positivity_colorScale}
      />
    </Svg>

    <Html>
      <DotTrendTooltip
        dataset={ positivity }
      />
    </Html>
  </LayerCake>
</div>

  <div class="title">
<p><b>What this Chart Means</b>

<br>The positivity rate is the percentage of tests that returned positive for the virus. The day used is the day that the results were announced. Very high positivity rates have been seen in the hardest-hit parts of the country, but Oregon's rate is lower than the rate in the U.S. as a whole. The national rate has been<a  target="_blank" href="https://www.theatlantic.com/technology/archive/2020/04/us-coronavirus-outbreak-out-control-test-positivity-rate/610132/"> estimated to be 20%</a>.</p>
<p><b>Notes:</b> This isn't calculated for April 22-23, when the state delayed reporting negative cases due to a technical issue. The black line is a 7-day moving average. </p>
</div>

<div class="data-container" style="margin-top:20px; height: 80px;">
<p class="byline"><b>Sources:</b> Population estimates as of July, 1 2019, <a  target="_blank" href="https://www.pdx.edu/prc/population-reports-estimates">PSU</a>. Case and deaths are from the <a  target="_blank" href="https://govstatus.egov.com/OR-OHA-COVID-19">Oregon Health Authority</a>. 
</p>
</div>


