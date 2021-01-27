<script>
  import { LayerCake, Svg, Html } from 'layercake';
  import { scaleOrdinal } from 'd3-scale';
   import { scaleLog, scaleBand } from 'd3-scale';
  import { timeParse, timeFormat } from 'd3-time-format';

  import BarTrend from './components/BarTrend.svelte';
 
  import BarTrendTooltip from './components/BarTrendTooltip.svelte';


  import AxisX from './components/AxisX.svelte';
  import AxisY from './components/AxisY.svelte';
  import Labels from './components/Labels.svelte';

  import Tooltip from './components/Tooltip.svelte';
 
  import { onMount } from 'svelte';

  /* data */
  import coviddata from './data/coviddata_abbreviated.js'


  // As of 7.5 Wheeler have no cases at all
  const items = [
    {value: '41000', label: 'Oregon', group: 'State'},
    {value: '38900', label: 'Portland', group: 'Metro Areas'},
    {value: '41420', label: 'Salem', group: 'Metro Areas'},
    {value: '41001', label: 'Baker County', group: 'Counties'},
    {value: '41003', label: 'Benton County', group: 'Counties'},
    {value: '41005', label: 'Clackamas County', group: 'Counties'},
    {value: '41007', label: 'Clatsop County', group: 'Counties'},
    {value: '41009', label: 'Columbia County', group: 'Counties'},
    {value: '41011', label: 'Coos County', group: 'Counties'},
    {value: '41013', label: 'Crook County', group: 'Counties'},
    {value: '41015', label: 'Curry County', group: 'Counties'},
    {value: '41017', label: 'Deschutes County', group: 'Counties'},
    {value: '41019', label: 'Douglas County', group: 'Counties'},
    {value: '41021', label: 'Gilliam County', group: 'Counties'},
    {value: '41023', label: 'Grant County', group: 'Counties'},
    {value: '41025', label: 'Harney County', group: 'Counties'},
    {value: '41027', label: 'Hood River County', group: 'Counties'},
    {value: '41029', label: 'Jackson County', group: 'Counties'},
    {value: '41031', label: 'Jefferson County', group: 'Counties'},
    {value: '41033', label: 'Josephine County', group: 'Counties'},
    {value: '41035', label: 'Klamath County', group: 'Counties'},
    {value: '41037', label: 'Lake County', group: 'Counties'},
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
    {value: '41069', label: 'Wheeler County', group: 'Counties'},
    {value: '41071', label: 'Yamhill County', group: 'Counties'}
  ];


  let active = 'Cases';
  //let active = 'Hospitals';

  $: active, handleViewChange();


  let dialog;
  let submitdialog;

  let explainer_text = '';
  let hospital_explainer = '';
  let region_text = '';
  let region_pop_data = {};

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
  let dead_v_cases;  // Only do this for the whole state. 


  let has_deaths = false;

  let cases_long;
  let cases_series;
  let cases_domain;


  let new_deaths_long;
  let new_deaths_series;
  let new_deaths_domain;

  let new_cases_long;
  let new_cases_series;
  let new_cases_domain;




  let colorScale;
  let cases_colorScale;
  let deaths_colorScale;
  let new_deaths_colorScale;

  let new_cases_colorScale;
  let tests_colorScale;


  let isClearable = false;

  let epoch_start = new Date(2020, 2, 20);
  let epoch_end = new Date(2020, 3, 29);




  let epoch_domain = [epoch_start, epoch_end];


  let full_domain = [];


  let state_rate_dict = {};

  let max_date;

  let max_date_string = get_max_date_string();
  let current_value = coviddata['41000'][max_date_string]['n_c'];
  let current_value_formatted = addCommas(current_value)
  let chart_start = deltaDate(max_date, -36,0,0)
  // chart_start.setDate(max_date.getDate()-36);

  function deltaDate(input, days, months, years) {
      return new Date(
        input.getFullYear() + years, 
        input.getMonth() + months, 
        Math.min(
          input.getDate() + days,
          new Date(input.getFullYear() + years, input.getMonth() + months + 1, 0).getDate()
        )
      );
  }



  // Sometimes the hospital data is different
  let max_hosp_date_string;
  let max_hosp_date; 


  const map_colors = ['#ffdecc', '#ffc09c', '#ffa06b', '#ff7a33'];


  let selectedFIPS = '41000';
  let regionDisplay = 'Oregon statewide';

  // Hmm... https://stackoverflow.com/questions/56983938/in-svelte-how-to-console-logyes-when-a-variable-changed
  //$: selectedFIPS, handleSelect(selectedFIPS);

  let results_for_table = [];

  function format_number(num) {
    var num_raw = num.toLocaleString()
    var num_parts = num_raw.toString().split(".");
    num_parts[0] = num_parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return num_parts.join(".");
  }

  function addCommas (num) {
    const parts = String(num).split('.');
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return parts.join('.');
  }

  function format_rate(num) {
    return parseFloat(num.toFixed(1));
  }

  function format_date_string(this_date_string) {
    var dsparts = this_date_string.split("_");
    var result = String(parseInt(dsparts[1])) + "/" + parseInt(dsparts[2], 10);
    return result;
  }

  
  function get_max_date_string() {
    var this_jurisdiction = coviddata['41000'];

    var mdatestring = '';

     Object.keys(this_jurisdiction).sort().forEach(function(key) {
      if (key.startsWith('202')) {

        var key_parts = key.split("_")
        var month = parseInt(key_parts[1]);
        var year = parseInt(key_parts[0]);
        var day = parseInt(key_parts[2]);

        var this_date = new Date(year, month-1, day);



        if (key > mdatestring || !mdatestring) {
          mdatestring = key;
          max_date = this_date;
        }
      }
    })

    return mdatestring;

  }


  function prep_data_from_archive(data_type, fips) {

    var data_for_this_fips = [];
    var this_jurisdiction = coviddata[fips];
    var day_count = 0;

    var new_case_ma = [-1,-1,-1,-1,-1,-1,-1];
    var new_death_ma = [-1,-1,-1,-1,-1,-1,-1];



    Object.keys(this_jurisdiction).sort().forEach(function(key) {
      if (key.startsWith('202')) {
        day_count += 1;
        var key_parts = key.split("_")

        var month = parseInt(key_parts[1]);
        var year = parseInt(key_parts[0]);
        var day = parseInt(key_parts[2]);

        var this_date = new Date(year, month-1, day);


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
            if (this_date > chart_start) {

                data_for_this_fips.push({'month':this_date, 'New Cases':new_case_count, 'Trend':this_average});
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


            if (this_date > chart_start) {

              data_for_this_fips.push({'month':this_date, 'New Deaths':new_death_count, 'Trend':this_average});
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
  // #c4cf22 lime 
  // #00749b feature blue
  // #adb642 celery
  //  #cbd0d2 
  // 

  var seriesColors = [
    '#c4cf22',
    '#c4cf22',

  ];


  var seriesColors2 = [
    '#c4cf22',
    '#00749b',

  ];



  function handleViewChange() {
    
  }

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
    new_cases = prep_data_from_archive('new_cases', fips);
    new_deaths = prep_data_from_archive('new_deaths', fips);

    new_cases_long = get_long_data(new_cases);
    new_cases_series = get_series_names(new_cases);
    new_cases_domain = get_domain(new_cases_long,false);


    new_deaths_long = get_long_data(new_deaths);
    new_deaths_series = get_series_names(new_deaths);
    new_deaths_domain = get_domain(new_deaths_long,false);


    new_cases_colorScale = scaleOrdinal()
      .domain(new_cases_series)
      .range(seriesColors);


    new_deaths_colorScale = scaleOrdinal()
      .domain(new_deaths)
      .range(seriesColors2);

    }

  set_data('41000');
  let max_date_formatted = format_date_string(max_date_string);

  let now = new Date();
  let onejan = new Date(now.getFullYear(), 0, 1);


  function formatTickX (d) {
    const date = new Date(d);
    var day = date.getDate();
   

   
   return monthNames[date.getMonth()]  + date.getUTCDate();
    //return date.getMonth()+1 + "/" + date.getUTCDate();
  
  }
  
  function formatTickY (d) {
    if (d > 999) {
      return d / 1000 + 'k';
    }
    return d;
  }

  const parseDate = timeParse('%Y-%m-%d');


  let x_ticks = [];



  //x_ticks.push(new_cases[3][xKey]);
  //x_ticks.push(new_cases[32][xKey]);

  x_ticks.push(parseDate('2021-01-01'));


  console.log("xticks " );
  // x_ticks = [x_ticks[1], x_ticks[4]];
  console.log(x_ticks);




  function format_date(this_date) {
    return monthNames[this_date.getMonth()] + " " + this_date.getDate();
  }



  let casenumberfontsize = "50px";
  let shotcountfontsize = "18px";
  let totalfontsize = "24px";
  let chartcontainerheight = "200px";
  let charttopheight = "0px;"
  let shownumbercontainer = true;
  let showcharttopcontainer = false;
  let chartcontainerwidth = "60%";
  let numbercontainerwidth = "37%";

  let num_x_ticks = 3;
  let num_y_ticks = 3;


  function set_font_sizes() {
      
    var maindiv = document.getElementById('containerbase');
    var mainwidth = maindiv.offsetWidth;



    if (mainwidth <= 250) {
      casenumberfontsize = "26px";
      shotcountfontsize = "12px";

      chartcontainerwidth = "99%";
      numbercontainerwidth = "0%";

      shownumbercontainer = false;
      showcharttopcontainer = true;


      chartcontainerheight = "160px";
      charttopheight = "40px";


      return 0;
    }

    if (mainwidth <= 300) {
      casenumberfontsize = "26px";
      shotcountfontsize = "14px";

      chartcontainerwidth = "60%";
      numbercontainerwidth = "37%";

      shownumbercontainer = true;
      showcharttopcontainer = false;

      chartcontainerheight = "200px";
      charttopheight = "0px";

      return 0;

    } 


    if (mainwidth <= 350) {
      casenumberfontsize = "32px";
      shotcountfontsize = "14px";
      chartcontainerwidth = "60%";
      numbercontainerwidth = "37%";
      shownumbercontainer = true;
      showcharttopcontainer = false;

      chartcontainerheight = "200px";
      charttopheight = "0px";
      return 0;

    }

    casenumberfontsize = "36px";
    shotcountfontsize = "18px";

    chartcontainerwidth = "60%";
    numbercontainerwidth = "37%";
    shownumbercontainer = true;
    showcharttopcontainer = false;
    chartcontainerheight = "200px";
    charttopheight = "0px";

  }



  var pymChild = new pym.Child();

  function setExplicitHeight(height) {  
    // We can ignore pym's estimate of the height and send our own. 
    pymChild.sendMessage('height', height);
    console.log("Pym: sent user chosen height of " + height);
  }





  onMount(() => {
    window.addEventListener('resize', set_font_sizes);
    setTimeout(set_font_sizes, 50);
    setExplicitHeight(200);

  });

</script>

<style>




  .chart-container {
    width: 99%;
    font-weight:400;

  }

  .chart-container-exterior {

    max-width: 400px;
    height: 200px;
    float:right;
  }

  .chart-top {
    margin:0px;
    padding: 0px;
  }

  .number-container {
    float:left;
    font-weight: 400;


  }

  .casenumber {
    display: flex;
  justify-content: center;
  align-items: center;
    font-family:'Roboto';
    font-size: 50px;
    height: 110px;
  }
  .casedate {
    font-family:'Roboto';
    height: 85px;
    text-align: center;
  }
  .date {
    font-size: 24px;
  }
  .weekly {
    font-family:'Roboto';
    font-size: 16px;
  }
  .numberdisplay {
    background-color:#CCC;
  }

  .wholecontainer {
    max-width: 500px;
  }

  .casenumbertop {
    width: 99%;
    text-align: center;
    font-weight:700;


  }

  .casedatetop {
    width: 99%;
    text-align: center;

  }

</style>

<div class="wholecontainer" id="containerbase">
  <div class="float-container">

    {#if shownumbercontainer}
    <div class="number-container" style="width: 37%;">
      <div class="number-top">
        <div class="casenumber">
          <span style="font-size:{casenumberfontsize}; font-weight:700;">+{current_value_formatted}</span>
        </div>
      </div>
              
      <div class="casedate">
        <span style="font-size:{shotcountfontsize};">Cases reported {format_date(max_date)}</span>
      </div>
    </div>
    {/if}

    <div class="chart-container-exterior" style="width: {chartcontainerwidth};">

      {#if showcharttopcontainer}
      <div class="chart-top" style="height: {charttopheight};">
        <div class="casenumbertop">
          <span style="font-size:{casenumberfontsize}; font-weight:700;">+{current_value_formatted}</span>
        </div>
                
        <div class="casedatetop">
          <span style="font-size:{shotcountfontsize};">Cases reported {format_date(max_date)}</span>
        </div>
      </div>
      {/if}


      <div class="chart-container" style="height: {chartcontainerheight};">
        
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
              ticks={x_ticks}
              formatTick={formatTickX}
              snapTicks={false}
              tickNumber=3
            />
            <AxisY
              formatTick={formatTickY}
              tickNumber=2
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

    </div> <!--- chart-container-exterior -->

  </div>  <!--- float-container -->

</div> <!---  wholecontainer -->




