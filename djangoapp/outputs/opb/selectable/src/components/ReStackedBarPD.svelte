<script>
	import { getContext } from 'svelte';
	const { data, xGet, yGet, height, width, xDomain } = getContext('LayerCake');
	export let colorScale = d => '#000';


	$: columnHeight = d => {
		return $height - $yGet(d);
	};

	const columnWidth2 = (1/2)*$width / $data[0]['values'].length;



  	// To calculate the time difference of two dates 
	var Difference_In_Time = $xDomain[1].getTime() - $xDomain[0].getTime(); 
  
	// To calculate the no. of days between two dates 
	var Difference_In_Days = Difference_In_Time / (1000 * 3600 * 24); 

	const columnWidth =  ( $data[2]['values'].length / Difference_In_Days) * ( $width / $data[0]['values'].length );

  // #c4cf22 lime 
  // #00749b feature blue
  // #adb642 celery
  //  #cbd0d2 
  // #b01417 dark red


	const fill2 = '#c4cf22';
	const fill1 = '#b01417';


	const stroke = '#333333';
	const strokeWidth = 1;
	const barstroke1 = '#cccccc';
	const barstroke2 = '#cccccc';

	const r = 4;




</script>


<g class="column-group">
	{#each $data[2]['values'] as d, i}
		{#if d['Suspected']!=-1 }
		<rect
			class='group-rect'
			data-id="{i}"
			x="{$xGet(d)-columnWidth/2}"
			y="{$yGet(d)}"
			width="{columnWidth}"
			height="{columnHeight(d)}"
			fill="{fill2}"
			stroke="{barstroke1}"
			stroke-width="{strokeWidth}"
		></rect>
		{/if}
	{/each}
</g>


<g class="column-group">
	{#each $data[1]['values'] as d, i}

		<rect
			class='group-rect'
			data-id="{i}"
			x="{$xGet(d)-columnWidth/2}"
			y="{$yGet(d)}"
			width="{columnWidth}"
			height="{columnHeight(d)}"
			fill="{fill1}"
			stroke="{barstroke2}"
			stroke-width="{strokeWidth}"
		></rect>
	{/each}
</g>










<style>
	.path-line {
		fill: none;
		stroke-linejoin: round;
		stroke-linecap: round;
		stroke-width: 3px;
	}
</style>
