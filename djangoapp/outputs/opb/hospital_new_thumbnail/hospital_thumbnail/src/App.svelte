<script>
  import MapScale from './components/MapScale.svelte';
  import AxisXScaleBand from './components/AxisXScaleBand.svelte';
  import { onMount } from 'svelte';

  import { LayerCake, Svg, Html, flatten } from 'layercake';
  import { stack } from 'd3-shape';
  import { scaleBand, scaleOrdinal } from 'd3-scale';
  import { format, precisionFixed } from 'd3-format';

  import BarStacked from './components/BarStacked.svelte';
  import AxisX from './components/AxisX.svelte';
  import AxisY from './components/AxisY.svelte';
  import Annotations from './components/Annotations.svelte'

  //import hospitaldata from './data/hospitals_live.csv';
  import hospitaldata from './data/hospitals_blank.csv';
  import Papa from 'papaparse';



  let annotations;
  let icu_covid_prcnt = 0;
  let all_covid_prcnt = 0;
  let data;
  //const csv_url='https://jf-cloudfront.s3.amazonaws.com/opb/V2.0/thumbnails/hospitals_thumbnail/data/hospitals-live.csv';

  const csv_url="hospitals-live.csv?12"

  


  const xKey = [0, 1];
  const yKey = 'name';
  const zKey = 'key';

  let series;
  //const seriesColors = ['#00749b', '#c4cf22', '#727475'];
  const seriesNames = Object.keys(hospitaldata[0]).filter(d => d !== yKey);
  const seriesColors = ['#00bbff', '#8bcef6', '#eff2f3'];

  const stackData = stack()
    .keys(seriesNames);

  function set_chart_data(rawdata) {

    delete rawdata[0].updated;
    delete rawdata[1].updated;

    data = rawdata;

    data.forEach(j => {
      ['covid', 'other', 'available'].forEach(k => {
        j[k] = parseFloat(j[k]);
        if (k=='covid') {
          if (j['name'] == 'All' ) {
            all_covid_prcnt = j[k];
          }
          if (j['name'] == 'ICU' ) {
            icu_covid_prcnt = j[k];
          }

        }
      })
    })

    data.forEach(d => {
      seriesNames.forEach(name => {
        d[name] = +d[name];
      });
    });

    series = stackData(data);
    annotations = [
      {
        text: all_covid_prcnt + '%',
        bottom: '20%',
        left: '2%',
      },
      {
        text:  icu_covid_prcnt + '%',
        bottom: '72%',
        left: '2%',
      }
    ];
  }

  set_chart_data(hospitaldata);

  const formatTickX = d => format(`.${precisionFixed(d)}s`)(d);

  let labels = []
  let breaks =  [] 
  let table_variable_name = 'New';
  let scaleword = "new cases";

  var label_array = [];

  const map_colors = seriesColors;

  function set_labels() {

    labels = [
      {'label':'COVID'},
      {'label':'Other'},
      {'label':'Free'},
    ]

    label_array = [];

    labels.forEach(row => {
      row.value = 1;
      label_array.push(row.label);
    });
  }

  function set_breaks(these_breaks) {
    breaks = these_breaks;
    set_labels();
  }

  set_breaks([1,2,3], 'dpm');


  var pymChild = new pym.Child();

  function setExplicitHeight(height) {  
    // We can ignore pym's estimate of the height and send our own. 
    pymChild.sendMessage('height', height);
  }

  onMount(async () => {

    // The raw sheet gives numbers as text strings
    // but these get parsed in set_chart_data
    Papa.parse(csv_url, {
      download: true,
      header: true,
      complete: function(results) {
        var rawdata = results['data']
        var update_date = rawdata[0].updated;
        console.log("Last updated date: " + update_date + ". OHA does not update this on weekends or holidays.");
        set_chart_data(rawdata);
      }
    });
  });

 



</script>

<style>
  .chart-container {
    width: 100%;
    max-width: 500px;
    height: 150px;
  }

  .scale_container {
    margin-top:10px;
    margin-right:10px;
    width: 98%;
    max-width: 500px;
    height: 30px;
  }
  .container {
    height: 200px;
    width: 100%;
    margin:0px;
    padding:0px;
  }
 body {
          font-family: 'Roboto', sans-serif;
        }

</style>
<div class="container">

<div class="chart-container">
  <LayerCake
    padding={{ top: 0, bottom: 20, left: 50, right: 20}}
    x={xKey}
    y={d => d.data[yKey]}
    z={zKey}
    yScale={scaleBand().paddingInner([0.05]).round(true)}
    yDomain={['All', 'ICU']}
    zScale={scaleOrdinal()}
    zDomain={seriesNames}
    zRange={seriesColors}
    flatData={flatten(series)}
    data={series}
  >
    <Svg>
      <AxisX
        baseline={false}
        snapTicks={false}
        formatTick={formatTickX}
      />
      <AxisY
        gridlines={false}
      />
      <BarStacked/>
    </Svg>
    <Html>
      <Annotations {annotations}/>
    </Html>
  </LayerCake>
</div>

<div class="scale_container">
  <LayerCake
      padding={{ top: 0, right: 0, bottom: 20, left:0 }}
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
</div>

</div>