<script>
  import { LayerCake, Svg, Html } from 'layercake';
  import { scaleOrdinal } from 'd3-scale';
   import { scaleLog, scaleBand } from 'd3-scale';

  import MultiLine from './components/MultiLine.svelte';
  import BarTrend from './components/BarTrend.svelte';
  import DotTrend from './components/DotTrend.svelte';

  import ReStackedBar from './components/ReStackedBar.svelte';
  import ReStackedBarTooltip from './components/ReStackedBarTooltip.svelte';

  import BarTrendTooltip from './components/BarTrendTooltip.svelte';
  import DotTrendTooltip from './components/DotTrendTooltip.svelte';

  import ReStackedBarPD from './components/RestackedBarPD.svelte';
  import ReStackedBarPDTooltip from './components/RestackedBarPDTooltip.svelte';


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
  import hospitalizeddata from './data/everhospitalized.js'
  import coviddetails from './data/coviddetails.js'

  /* svelte smui */



  import Tab, {Label as TabLabel} from '@smui/tab';
  import TabBar from '@smui/tab-bar';

  
  import {MDCSelect} from '@material/select';
  import Select, { Option } from "@smui/select";

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
    //{value: '41069', label: 'Wheeler County', group: 'Counties'},
    {value: '41071', label: 'Yamhill County', group: 'Counties'}
  ];


  // the selected item is temporarily removed from the list when selected
  // make a lookup for it. 
  var itemlookup = {};
  items.forEach(function (item, index) {
    itemlookup[item.value] = item.label;
  });


  let active = 'Cases';
  $: active, handleViewChange();


  let dialog;
  let submitdialog;

  let explainer_text = '';
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

  let epoch_start = new Date(2020, 2, 20);
  let epoch_end = new Date(2020, 3, 29);

  let epoch_domain = [epoch_start, epoch_end];

  let total_hospitalized;
  let total_hospitalized_long
  let total_hospitalized_series;
  let total_hospitalized_domain;
  let total_hospitalized_colorScale;


  let current_hospitalized; 
  let current_hospitalized_long
  let current_hospitalized_series;
  let current_hospitalized_domain;

  let current_icu; 
  let current_icu_long
  let current_icu_series;
  let current_icu_domain;
  let current_icu_colorScale;


  let current_vent; 
  let current_vent_long
  let current_vent_series;
  let current_vent_domain;
  let current_vent_colorScale;

  let current_hospitalized_colorScale;

  let full_domain = [];


  let state_rate_dict = {};

  let max_date_string;
  let max_date;


  const map_colors = ['#ffdecc', '#ffc09c', '#ffa06b', '#ff7a33'];

  let recent_date_text = 'May 2 at 8 a.m.'

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


    region_text = regionDisplay + " reported a total of " + format_number(coviddata[thisfips][max_date_string]['c']) + " confirmed cases and " + format_number(coviddata[thisfips][max_date_string]['d']) + " deaths as of " + format_date_string(max_date_string) + ", including a daily net increase in total cases of <b>" + coviddata[thisfips][max_date_string]['n_c'] +"</b> and <b>" + coviddata[thisfips][max_date_string]['n_d'] + "</b> new death" + death_plural + "."; 


    has_deaths = coviddata[thisfips][max_date_string]['d'] > 0;
    

    // Assumes that pymchild is defined on the page before here! 
    setTimeout(function(){ pymChild.sendHeight(); }, 20);
    //console.log("height sent");

    console.log(cases_long);
  }

  function prep_covid_details(data_type) {
    var data_to_return = [];

    Object.keys(coviddetails).forEach(function(key) {
      var this_data = coviddetails[key];

      var key_parts = key.split("_")

      var month = parseInt(key_parts[1]);
      var year = parseInt(key_parts[0]);
      var day = parseInt(key_parts[2]);

      // javascript has a month implementation bug
      var this_date = new Date(year, month-1, day);

      if (data_type == 'current_hospitalized') {

          var suspected = 0;
          var confirmed = this_data['h_c'];
          var total = this_data['h_t'];

          if (this_data['h_c'] == '-1') {
            confirmed = 0;
          } else {
            suspected = total - confirmed;
          }

          if (this_data['h_t'] == '-1') {
            total = 0;
          }
          if (this_data['h_s'] == '-1') {
            suspected = 0;
          }
        if (this_data['h_t'] != '-1') {
            data_to_return.push({'month':this_date, 'Suspected':suspected, 'Confirmed':confirmed, 'Total':total,});
          }
        full_domain.push({'month':this_date})

        }

      if (data_type == 'current_icu') {
          var suspected = 0;
          var confirmed = this_data['i_c'];
          var total = this_data['i_t'];

          if (this_data['i_c'] == '-1') {
            confirmed = 0;
          } else {
            suspected = total - confirmed;
          }

          if (this_data['i_t'] == '-1') {
            total = 0;
          }
          if (this_data['i_s'] == '-1') {
            suspected = 0;
          }
        if (this_data['i_t'] != '-1') {
            data_to_return.push({'month':this_date, 'Suspected':suspected, 'Confirmed':confirmed, 'Total':total,});
          }
      }

      if (data_type == 'current_vent') {
          var suspected = 0;
          var confirmed = this_data['v_c'];
          var total = this_data['v_t'];

          if (this_data['v_c'] == '-1') {
            confirmed = 0;
          } else {
            suspected = total - confirmed;
          }

          if (this_data['v_t'] == '-1') {
            total = 0;
          }
          if (this_data['v_s'] == '-1') {
            suspected = 0;
          }
        if (this_data['v_t'] != '-1') {
            data_to_return.push({'month':this_date, 'Suspected':suspected, 'Confirmed':confirmed, 'Total':total,});
          }
      }



      });

      return data_to_return;
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

        var this_date = new Date(year, month-1, day);


        if (key > max_date_string || !max_date_string) {
          max_date_string = key;
          max_date = this_date;

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
            //console.log("day count: " + day_count + " this date " + this_date);
            // futzing with this, cleanup when we know how it should work
            if (day_count == 34 || day_count == 35  || day_count == 99  || day_count == 100 || day_count == 106 || day_count == 107 ) {
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

            if (day_count != 34 && day_count != 35 && day_count != 99 && day_count != 100 && day_count != 106  || day_count == 107) {
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


        if (data_type == 'total_hospitalized') {
          var this_data = {'month':this_date};
          var this_hospitalized = -1;
          if (key in hospitalizeddata) {
            this_hospitalized = parseInt(hospitalizeddata[key]['yes']);
          }
          if (day_count > 1 && this_hospitalized > 0) {
            data_for_this_fips.push({'month':this_date, 'Hospitalized':this_hospitalized});
          }
        }



        if (data_type == 'dead_v_cases') {
          var this_data = {'month':this_date};

          var this_hospitalized = -1;

          if (key in hospitalizeddata) {

            this_hospitalized = parseInt(hospitalizeddata[key]['yes']);

          }
          
          if (day_count > 1) {
            if (this_jurisdiction[key]['d'] > 0 && this_jurisdiction[key]['c']) {
              data_for_this_fips.push({'month':this_date, 'Deaths':this_jurisdiction[key]['d'], 'Cases':this_jurisdiction[key]['c'], 'Hospitalized':this_hospitalized});
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
    //console.log("handleViewChange send height");
    setTimeout(function(){ pymChild.sendHeight(); }, 50);
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


    deaths_long = get_long_data(deaths);
    deaths_series = get_series_names(deaths);
    deaths_domain = get_domain(deaths_long,false);

    new_deaths_long = get_long_data(new_deaths);
    new_deaths_series = get_series_names(new_deaths);
    new_deaths_domain = get_domain(new_deaths_long,false);



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
  epoch_domain = [epoch_start, max_date];



  function set_sitewide_charts(){
    //Run this once, these are not regenerated
    dead_v_cases = prep_data_from_archive('dead_v_cases', '41000');

    dead_v_cases_long = get_long_data(dead_v_cases);
    dead_v_cases_series = get_series_names(dead_v_cases);
    dead_v_cases_domain = get_domain(dead_v_cases_long,true);

    dead_v_cases_colorScale = scaleOrdinal()
      .domain(dead_v_cases_series)
      .range(seriesColors);

    total_hospitalized = prep_data_from_archive('total_hospitalized', '41000');
    total_hospitalized_long = get_long_data(total_hospitalized);
    total_hospitalized_series = get_series_names(total_hospitalized);
    total_hospitalized_domain = get_domain(total_hospitalized_long,false);

    total_hospitalized_colorScale = scaleOrdinal()
      .domain(total_hospitalized_series)
      .range(seriesColors);


    var portland_cases = coviddata['38900'][max_date_string]['c'];
    var salem_cases = coviddata['41420'][max_date_string]['c'];
    var ros_cases = coviddata['41000'][max_date_string]['c'] - portland_cases - salem_cases;

    region_pop_data['metro_pop'] = coviddata['38900']['pop'] + coviddata['41420']['pop'];
    region_pop_data['rest_pop'] = coviddata['41000']['pop'] - region_pop_data['metro_pop'];  



    current_hospitalized = prep_covid_details('current_hospitalized');

    current_hospitalized_long = get_long_data(current_hospitalized);
    current_hospitalized_series = get_series_names(current_hospitalized);
    current_hospitalized_domain = get_domain(current_hospitalized_long,true);
  
    current_hospitalized_colorScale = scaleOrdinal()
      .domain(current_hospitalized_series)
      .range(seriesColors);


    current_icu = prep_covid_details('current_icu');
    current_icu_long = get_long_data(current_icu);
    current_icu_series = get_series_names(current_icu);
    current_icu_domain = get_domain(current_icu_long,true);
  
    current_icu_colorScale = scaleOrdinal()
      .domain(current_icu_series)
      .range(seriesColors);


    current_vent = prep_covid_details('current_vent');
    current_vent_long = get_long_data(current_vent);
    current_vent_series = get_series_names(current_vent);
    current_vent_domain = get_domain(current_vent_long,true);
  
    current_vent_colorScale = scaleOrdinal()
      .domain(current_icu_series)
      .range(seriesColors);



  }

  set_sitewide_charts();
  let now = new Date();
  let onejan = new Date(now.getFullYear(), 0, 1);

  function formatTickX (d) {
    const date = new Date(d);
    var day = date.getDate();
    if (day == 1) {
      if (date.getUTCMonth()  == 3 || date.getUTCMonth() == 9) {
        return `${monthNames[date.getUTCMonth()]} ${date.getUTCDate()}`;
      }
      else {
        return '';
      }
    }
    else {
        return '';
    }

    /*
    var dayofweek = date.getDay()
    if (dayofweek==5 ) {
      var weeknum = Math.ceil( (((date - onejan) / 86400000) + onejan.getDay() + 1) / 7 );
      if (weeknum%2==0) {
        return `${monthNames[date.getUTCMonth()]} ${date.getUTCDate()}`;
      }
      else {
        return '';
      }
    } else {
      return '';
    }
    */
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
<div style="margin-bottom: 20px;">
    <TabBar tabs={['Cases', 'Deaths', 'Hospitals']} let:tab bind:active>
      <Tab {tab} minWidth>
        <TabLabel>{tab}</TabLabel>
      </Tab>
    </TabBar>
  </div>
</div>


{#if active=='Cases' || active=='Deaths' }


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

{/if }


{#if active=='Cases' }

<div class="title">
<h3>New confirmed cases, {regionDisplay}</h3>
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

<b>What this chart means:</b><br>
<p> One key question is how quickly the virus is spreading. This chart shows lab-confirmed cases and state-designated "presumptive" cases, in which patients show COVID-like symptoms and have been in "close contact with a confirmed case". The actual number of cases is likely considerably higher.</p>
<p>The date shown is the day that the state announced the case, not the day that the person caught the virus. It may take several days to a week for results to become available, so this chart lags behind reality. People who catch the virus often recover within 21 days of becoming symptomatic, although less severe cases may pass quicker.</p>


<p><b>Notes:</b> The daily case count is the <b>difference</b> between total cases announced by OHA on consecutive days. Because some presumptive cases are eventually shown not to be cases, and subtracted from the count, the actual number of daily new cases may be slightly higher than shown. The black line is a 7-day moving average. </p>
</div>

<div class="title">
<h3>Total cases, {regionDisplay}</h3>
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
<p><b>What this chart means:</b> <br>When transmission of the virus stops, this chart will flatten out. Early indications are that social distancing has slowed the spread of the virus. This chart shows only laboratory-confirmed cases, so the total number of actual cases is significantly higher.</p>
</div>


<div class="title">
<h3>Daily test results, {regionDisplay}</h3>
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
<p><b>What this chart means</b>

<br>Widely available testing is one of the key requirements to ending social distancing, although epidemiologists argue it's <a  target="_blank" href="https://www.statnews.com/2020/03/24/we-need-smart-coronavirus-testing-not-just-more-testing/">not just the number of tests that matter</a>. One team at Harvard suggests reopening states would require <a  target="_blank" href="https://www.nytimes.com/interactive/2020/04/17/us/coronavirus-testing-states.html">152 tests per 100,000 residents</a>, which translates into more than 6,400 tests in Oregon daily.
</p>
<p><b>Notes:</b> On April 22, June 26 and July 4 authorities did not provide a negative test count.</p>
</div>


<div class="title">
<h3>Test positivity rate, {regionDisplay}</h3>
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
<p><b>What this chart means</b>

<br>The positivity rate is the percentage of tests that returned positive for the virus. The day used is the day that the results were announced. Very high positivity rates have been seen in the hardest-hit parts of the country, but Oregon's rate is lower than the rate in the U.S. as a whole. The national rate has been<a  target="_blank" href="https://www.theatlantic.com/technology/archive/2020/04/us-coronavirus-outbreak-out-control-test-positivity-rate/610132/"> estimated to be 20%</a>.</p>
<p><b>Notes:</b>  Beginning May 4, Oregon began including "presumptives" in the daily case count. This records someone lacking a positive test but who "is showing symptoms and has had close contact with a confirmed case". Including these cases artificially boosts the positivity rate on the day they are announced, although this should eventually even itself out when test results confirm it. The black line is a 7-day moving average. Days with missing negatives, as well as the following day (in which two days of negatives are effectively reported), are not shown or included in the trend line. </p>
</div>

{/if }

{#if active == 'Deaths' }

<div class="title">

<h3>New deaths, {regionDisplay}</h3>
<p>{explainer_text}</p>
<p>{@html region_text}</p>
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
        fill="#c4cf22"
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

<b>What this chart means:</b><br>
<p>This chart shows known deaths due to COVID-19. It is an undercount. In other areas total deaths have been adjusted upwards later to include deaths at home, in homeless camps, and where testing was not immediately available.</p>


<p><b>Notes:</b> The black line is a 7-day moving average. </p>
</div>


<div class="title">
<h3>Total deaths, {regionDisplay}</h3>
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
<p><b>What this chart means:</b><br> Our understanding of the virus is that people often become symptomatic 5-7 days after exposure. While the vast number survive, some <a href="https://www.thelancet.com/action/showPdf?pii=S0140-6736%2820%2930566-3" target="_blank">published reports</a> estimate the time from symptom onset until death to be 19 days, although this number varies. The effects of social distancing should be evident in deaths reported within about 25 days.</p>
</div>

{/if }

{#if active == 'Hospitals' }

<div class="title">
<p>Hospitalization data is only available statewide. Beginning June 6, the Oregon Health Authority stopped reporting hospitalization data on the weekends and holidays. </p>
</div>



<div class="title">
<h3>Current hospitalizations, Oregon statewide</h3>
</div>

<div class="chart-container">
  <LayerCake
    padding={{ top: 27, right: 10, bottom: 20, left: 40 }}
    x='month'
    y='value'
    xDomain={epoch_domain}
    yDomain={current_hospitalized_domain}
    flatData={flatten(current_hospitalized_long)}
    data={current_hospitalized_long}
  >
    <Svg>
      <AxisX
        gridlines={false}
        ticks={full_domain.map(d => d[xKey])}
        formatTick={formatTickX}
        snapTicks={true}
      />
      <AxisY
        formatTick={formatTickY}
      />

      <ReStackedBarPD
        colorScale={current_hospitalized_colorScale}
      />
    </Svg>

    <Html>
      <ReStackedBarPDTooltip
        dataset={ current_hospitalized }
      />
    </Html>
  </LayerCake>
</div>

 <div class="title">
<p><b>What this chart means</b>

<br>This chart shows the daily count of hospital beds filled by patients who are either confirmed to have the virus or are suspected of having it. There are about 7,500 hospital beds in OR, about 2,000 of which are available day-to-day.</p>


<p><b>Notes: </b>This data was not available before April 6.</p>

</div>



<div class="title">
<h3>Current ICU, Oregon statewide</h3>
</div>

<div class="chart-container">
  
  <LayerCake
    padding={{ top: 27, right: 10, bottom: 20, left: 40 }}
    x='month'
    y='value'
    xDomain={epoch_domain}
    yDomain={[0,130]}
    flatData={flatten(current_icu_long)}
    data={current_icu_long}
  >
    <Svg>
      <AxisX
        gridlines={false}
        ticks={full_domain.map(d => d[xKey])}
        formatTick={formatTickX}
        snapTicks={true}
      />
      <AxisY
        formatTick={formatTickY}
      />

      <ReStackedBarPD
        colorScale={current_icu_colorScale}
      />
    </Svg>

    <Html>
      <ReStackedBarPDTooltip
        dataset={ current_icu }
      />
    </Html>
  </LayerCake>
</div>

 <div class="title">
<p><b>What this chart means</b>

<br>This chart shows the total number of intensive care beds filled by patients who are either confirmed to have the virus or are suspected of having it. There are about 800 adult ICU beds in the state, about 300 of which are available day-to-day.</p>
<p><b>Notes: </b>This data was not available before April 8.</p>

</div>


<div class="title">
<h3>Current ventilator usage, Oregon statewide</h3>
</div>

<div class="chart-container">
  
  <LayerCake
    padding={{ top: 27, right: 10, bottom: 20, left: 40 }}
    x='month'
    y='value'
    xDomain={epoch_domain}
    yDomain={[0,82]}
    flatData={flatten(current_vent_long)}
    data={current_vent_long}
  >
    <Svg>
      <AxisX
        gridlines={false}
        ticks={full_domain.map(d => d[xKey])}
        formatTick={formatTickX}
        snapTicks={true}
      />
      <AxisY
        formatTick={formatTickY}
      />

      <ReStackedBarPD
        colorScale={current_vent_colorScale}
      />
    </Svg>

    <Html>
      <ReStackedBarPDTooltip
        dataset={ current_vent }
      />
    </Html>
  </LayerCake>
</div>

 <div class="title">
<p><b>What this chart means</b>

<br>This chart shows the total number of patients on mechanical ventilators who are either confirmed to have the virus or are suspected of having it. There are about 800 ventilators at hospitals in statewide.</p>

<p><b>Notes: </b>This data was not available before April 6.</p>

</div>



<div class="title">
<h3>Total hospitalized statewide</h3>
</div>

<div class="chart-container">
  
  <LayerCake
    padding={{ top: 27, right: 10, bottom: 20, left: 40 }}
    x='month'
    y='value'
    flatData={flatten(total_hospitalized_long)}
    yDomain={total_hospitalized_domain}
    data={total_hospitalized_long}
  >
    <Svg>
      <AxisX
        gridlines={false}
        ticks={total_hospitalized.map(d => d[xKey])}
        formatTick={formatTickX}
        snapTicks={true}
      />
      <AxisY
        formatTick={formatTickY}
      />

      <MultiLine
        colorScale={total_hospitalized_colorScale}
      />
    </Svg>

    <Html>
      <Tooltip
        dataset={ total_hospitalized }
      />
    </Html>
  </LayerCake>
</div>


<div class="title">
<p><b>What this chart means</b>
<br>This chart shows the cumulative total of COVID-positive patients who have ever been admitted to a hospital in Oregon. Data are provisional. <p></p>
<p><b>Notes: </b>The spike in hospitalizations around April 6 appears to reflect an error in provisional data that was later revised downwards.</p>
</div>


{/if }
<div class="data-container" style="margin-top:20px; height: 80px;">
<p class="byline"><b>Sources:</b> Population estimates as of July, 1 2019, <a  target="_blank" href="https://www.pdx.edu/prc/population-reports-estimates">PSU</a>. Case and deaths are from the <a  target="_blank" href="https://govstatus.egov.com/OR-OHA-COVID-19">Oregon Health Authority</a>. 
</p>
</div>


