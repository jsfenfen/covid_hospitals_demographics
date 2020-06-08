<script>
	import { getContext } from 'svelte';
	const { data, xGet, yGet } = getContext('LayerCake');
	export let colorScale = d => '#000';



	$: path = values => {


		return 'M' + values
			.map(d => {
				return $xGet(d) + ',' + $yGet(d);
			})
			.join('L');
	};

	function clean_values(values) {
		var new_values = [];
		for (var i=0; i<values.length; i++) {
			if (values[i]['value'] != -1) {
				new_values.push(values[i]);
			}
		}

		return new_values;

	}
</script>

<g class="line-group">
	{#each $data as group}
		<path
			class='path-line'
			d='{path(clean_values(group.values))}'
			stroke="{colorScale(group.key)}"
		></path>
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
