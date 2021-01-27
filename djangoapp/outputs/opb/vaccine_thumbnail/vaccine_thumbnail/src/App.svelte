<script>
  import { LayerCake, Svg, Html } from 'layercake';
  import { scaleOrdinal } from 'd3-scale';
  import { timeParse, timeFormat } from 'd3-time-format';
  import { format, precisionFixed } from 'd3-format';

  import MultiLine from './components/MultiLine.svelte';
  import AxisX from './components/AxisX.svelte';
  import AxisY from './components/AxisY.svelte';
  import Labels from './components/Labels.svelte';
  import SharedTooltip from './components/SharedTooltip.svelte';

  //import data from './data/vaccinations.csv';

  import vaccination_data from './data/vaccinations-live.csv';


  import { onMount } from 'svelte';

  /* --------------------------------------------
   * Set what is our x key to separate it from the other series
   */
  const xKey = 'date';
  const yKey = 'value';
  const zKey = 'key';



  let casenumberfontsize = "50px";
  let shotcountfontsize = "18px";
  let totalfontsize = "24px";
  let chartcontainerheight = "200px";
  let charttopheight = "0px;"
  let shownumbercontainer = true;
  let showcharttopcontainer = false;
  let chartcontainerwidth = "60%";
  let numbercontainerwidth = "37%";

  let x_ticks = [];
  let num_y_ticks = 3;


  const seriesNames = Object.keys(vaccination_data[0]).filter(d => (d !== xKey && d !== 'today'));


  //const seriesColors = ['#adb642', '#00749b', '#ff7ac7', '#eff2f3'];

  const seriesColors = ['#adb642', '#00749b', '#ff7ac7', '#eff2f3'];

    // #c4cf22 lime 
  // #00749b feature blue
  // #adb642 celery
  // #cd3227 red
  // #b01417 dark red
  //  #cbd0d2 medium gray 
  //  #727475 gray
  // #eff2f3 light gray


  const parseDate = timeParse('%Y-%m-%d');

  const dataLong = seriesNames.map(key => {
    return {
      key,
      values: vaccination_data.map(d => {
        d[xKey] = typeof d[xKey] === 'string' ? parseDate(d[xKey]) : d[xKey]; // Conditional required for sapper
        return {
          key,
          [yKey]: +d[key],
          [xKey]: d[xKey]
        };
      })
    };
  });

  var num_reports = vaccination_data.length;
  //x_ticks.push(vaccination_data[3][xKey]);
  //x_ticks.push(vaccination_data[num_reports-3][xKey]);


  x_ticks.push(parseDate('2021-01-01'));

  console.log("x_ticks");
  console.log(x_ticks);
  function set_font_sizes() {
    console.log("set_font_sizes");
      
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


  

  // Make a flat array of the `values` of our nested series
  // we can pluck the `value` field from each item in the array to measure extents
  const flatten = data => data.reduce((memo, group) => {
    return memo.concat(group.values);
  }, []);

  let max_date = vaccination_data[0]['date']
  let current_value = vaccination_data[0]['today'];

  for (var i=0; i<vaccination_data.length; i++) {
    
    var this_date = vaccination_data[i]['date'];
    if (this_date >= max_date) {
      max_date = this_date;
      current_value = vaccination_data[i]['today']
    } 
  }

 const monthNames = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.'];

  function formatTickX (d) {
    const date = new Date(d);
    var day = date.getDate();
   

   
   return monthNames[date.getMonth()] + date.getUTCDate();
    //return date.getMonth()+1 + "/" + date.getUTCDate();
  
  }

  
  function formatTickY (d) {
    //var d_string = format(`.${precisionFixed(d)}s`)(d);
    var d_string = (d/1000).toFixed(0);

    return d_string + "k";

  }

  function addCommas (num) {
    const parts = String(num).split('.');
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return parts.join('.');
  }

  function format_rate(num) {
    return parseFloat(num.toFixed(1));
  }

  function format_date(this_date) {
    return monthNames[this_date.getMonth()] + " " + this_date.getDate();
  }


  //const formatTickY = d => format(`.${precisionFixed(d)}s`)(d);


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
    height: 110px;
  }
  .casedate {
    font-family:'Roboto';
    height: 85px;
    text-align: center;
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



<div id="containerbase" class="wholecontainer">

<div class="float-container">

{#if shownumbercontainer}
  <div class="number-container" style="width: 37%;">
    <div class="number-top">
      <div class="casenumber">
        <span style="font-size:{casenumberfontsize}; font-weight:700;">+{addCommas(current_value)}</span>
      </div>
    </div>
    <div class="casedate">
      <span style="font-size:{shotcountfontsize};">Vaccinations reported {format_date(max_date)}</span>
    </div>
  </div>
{/if}


<div class="chart-container-exterior" style="width: {chartcontainerwidth};">

{#if showcharttopcontainer}

  <div class="chart-top" style="height: {charttopheight};">


      <div class="casenumbertop">
        <span style="font-size:{casenumberfontsize}; font-weight:700;">+{addCommas(current_value)}</span>
      </div>
            
    <div class="casedatetop">

      <span style="font-size:{shotcountfontsize};">Vaccinations reported {format_date(max_date)}</span>
      
    </div>


  </div>
{/if}

  <div class="chart-container" style="height: {chartcontainerheight};">
  <LayerCake
    padding={{ top: 7, right: 10, bottom: 20, left: 25 }}
    x={xKey}
    y={yKey}
    z={zKey}
    yDomain={[0, 500000]}
    zScale={scaleOrdinal()}
    zDomain={seriesNames}
    zRange={seriesColors}
    flatData={flatten(dataLong)}
    data={dataLong}
  >
    <Svg>
      <AxisX
        gridlines={false}
        ticks={x_ticks}
        formatTick={formatTickX}
        snapTicks={false}
        tickNumber=2
      />
      <AxisY
        ticks={num_y_ticks}
        formatTick={formatTickY}
      />
      <MultiLine/>
    </Svg>

    <Html>

      <Labels />
    </Html>
  </LayerCake>

  </div>
</div>

</div>
</div>