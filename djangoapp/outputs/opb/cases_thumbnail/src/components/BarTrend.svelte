<script>
	import { getContext } from 'svelte';
	const { data, xGet, yGet, height, width } = getContext('LayerCake');
	export let colorScale = d => '#000';

	export let fill = '#00749b';



	$: path = values => {
		return 'M' + values
			.map(d => {
				return $xGet(d) + ',' + $yGet(d);
			})
			.join('L');
	};

	$: columnHeight = d => {
		return $height - $yGet(d);
	};

	const columnWidth = $width / (2*$data[0]['values'].length);

	function fillcolor(num) {
		if (num == $data[0]['values'].length-1 || num == $data[0]['values'].length-8 || num == $data[0]['values'].length-15 || num == $data[0]['values'].length-22 || num == $data[0]['values'].length-29 || num == $data[0]['values'].length-36) {
			return "#00749b";
		}
		return "#eff2f3";
	}

	    // #c4cf22 lime 
  // #00749b feature blue
  // #adb642 celery
  // #cd3227 red
  // #b01417 dark red
  //  #cbd0d2 medium gray 
  //  #727475 gray
  // #eff2f3 light gray

  // transcendant blue 00bbff

	const stroke = '#36362b';
	const strokeWidth = 1;
	export let barstroke = '#cccccc';


	const r = 4;


</script>


<g class="column-group">
	{#each $data[0]['values'] as d, i}
		<rect
			class='group-rect'
			data-id="{i}"
			x="{$xGet(d)-columnWidth}"
			y="{$yGet(d)}"
			width="{columnWidth}"
			height="{columnHeight(d)}"
			fill="{fillcolor(i)}"
			stroke="{barstroke}"
			stroke-width="{strokeWidth}"
		></rect>
	{/each}
</g>


<g class="line-group">
		<path
			class='path-line'
			d='{path($data[1].values)}'
			stroke="{stroke}"
		></path>
</g>






<style>
	.path-line {
		fill: none;
		stroke-linejoin: round;
		stroke-linecap: round;
		stroke-width: 3px;
	}
</style>
