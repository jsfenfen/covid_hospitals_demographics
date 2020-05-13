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

  import ReStackedBar from './components/ReStackedBar.svelte';
  import ReStackedBarTooltip from './components/ReStackedBarTooltip.svelte';

  import ReStackedBarPD from './components/RestackedBarPD.svelte';
  import ReStackedBarPDTooltip from './components/RestackedBarPDTooltip.svelte';


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
  import coviddetails from './data/coviddetails.js'


  let bar_chart_case_data = []
  let region_pop_data = {}

  let dead_v_cases;  // Only do this for the whole state. 


  let dead_v_cases_long
  let dead_v_cases_series;
  let dead_v_cases_domain;


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

  let dead_v_cases_colorScale;
  let current_hospitalized_colorScale;

  let state_rate_dict = {};

  let full_domain = [];

  let max_date_string;
  let max_date;

  let epoch_start = new Date(2020, 2, 20);
  let epoch_end = new Date(2020, 3, 29);

  let epoch_domain = [epoch_start, epoch_end];

var labels = [
    {'label':'0'},
    {'label':'<400'},
    {'label':'<600'},
    {'label':'<800'},
    {'label':'<1,000'},
    {'label':'1,000+'}

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
    Object.keys(this_jurisdiction).sort().forEach(function(key) {
      if (key.startsWith('2020')) {
        day_count += 1;
        var key_parts = key.split("_")

        var month = parseInt(key_parts[1]);
        var year = parseInt(key_parts[0]);
        var day = parseInt(key_parts[2]);

        // javascript has a month implementation bug
        var this_date = new Date(year, month-1, day);

        if (key > max_date_string || !max_date_string) {
          max_date_string = key;
          max_date = this_date;
        }


      
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

        if (data_type == 'total_hospitalized') {
          var this_data = {'month':this_date};
          var this_hospitalized = -1;
          if (key in hospitalizeddata) {
            this_hospitalized = parseInt(hospitalizeddata[key]['yes']);
          }
          if (day_count > 1) {
            data_for_this_fips.push({'month':this_date, 'Hospitalized':this_hospitalized});
          }
        }

        if (data_type == 'dead_v_cases') {
          var this_data = {'month':this_date};

          var this_hospitalized = -1;

          if (key in hospitalizeddata) {
            //console.log("hospitalization data for " + this_date );
            //console.log(hospitalizeddata[key]);

            this_hospitalized = parseInt(hospitalizeddata[key]['yes']);

          }
          //} else {
          //  console.log("no hospitalization data for " + key );
          //}
          
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
  }

  set_sitewide_charts();
  console.log("total_hospitalized");
  console.log(total_hospitalized);

  function set_data() {

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

  set_data();
  epoch_domain = [epoch_start, max_date];

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
    if (rate < 400) {
      return map_colors[1];
    }
    if (rate < 600) {
      return map_colors[2];
    }
    if (rate < 800) {
      return map_colors[3];
    }
    if (rate < 1000) {
      return map_colors[4];
    }
    return map_colors[5];
  }


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
<h3>Total Hospitalized Statewide</h3>
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
      <Labels/>
      <Tooltip
        dataset={ total_hospitalized }
      />
    </Html>
  </LayerCake>
</div>


<div class="title">
<p><b>What this Chart Means</b>
<br>This chart shows the cumulative total of COVID-positive patients who have ever been admitted to a hospital. <p></p>
<p><b>Notes: </b>The spike in hospitalizations around April 6 appears to reflect an error in the data that was later corrected.</p>
</div>


<div class="title">
<h3>Deaths, Cases and Hospitalizations</h3>
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


   <div class="title">
<p><b>What this Chart Means</b>

<br>This chart shows the cumulative total of cases, deaths, and COVID-positive patients who have ever been admitted to a hospital on a logarithmic scale. <p></p>
<p><b>Notes: </b>The spike around April 6 in total hospitalized appears to reflect an error in the data that was later corrected.</p>
</div>



<div class="title">
<h3>Current Hospitalizations, Oregon Statewide</h3>
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

      <ReStackedBar
        colorScale={current_hospitalized_colorScale}
      />
    </Svg>

    <Html>
      <ReStackedBarTooltip
        dataset={ current_hospitalized }
      />
    </Html>
  </LayerCake>
</div>

 <div class="title">
<p><b>What this Chart Means</b>

<br>This chart shows the daily count of hospital beds filled by patients who are either confirmed to have the virus or are suspected of having it. There are about 7,500 hospital beds in OR, about 2,000 of which are available day-to-day.</p>


<p><b>Notes: </b>This data was not available before April 6.</p>

</div>



<div class="title">
<h3>Current ICU, Oregon Statewide</h3>
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
<p><b>What this Chart Means</b>

<br>This chart shows the total number of intensive care beds filled by patients who are either confirmed to have the virus or are suspected of having it. There are about 800 adult ICU beds in the state, about 300 of which are available day-to-day.</p>
<p><b>Notes: </b>This data was not available before April 8.</p>

</div>


<div class="title">
<h3>Current Ventilator Usage, Oregon Statewide</h3>
</div>

<div class="chart-container">
  
  <LayerCake
    padding={{ top: 27, right: 10, bottom: 20, left: 40 }}
    x='month'
    y='value'
    xDomain={epoch_domain}
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
<p><b>What this Chart Means</b>

<br>This chart shows the total number of patients on mechanical ventilators who are either confirmed to have the virus or are suspected of having it. There are about 800 ventilators at hospitals in statewide.</p>

<p><b>Notes: </b>This data was not available before April 6.</p>

</div>
