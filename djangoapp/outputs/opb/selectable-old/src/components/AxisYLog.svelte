<script>
	import { getContext } from 'svelte';

	const { padding, yScale } = getContext('LayerCake');

	export let ticks = undefined;
	export let gridlines = true;
	//export let formatTick = d => d;

	export let tickNumber = 5;

	var display_chars = ['1', '2', '5'];

	function shouldDisplay(d) {
		var dstring = d.toString();
		var firstchar = dstring[0]
		if (display_chars.includes(firstchar)) 	{
			return true;
		} 
		return false;
	}

	function formatTick(d) {
		if (shouldDisplay(d) ) 	{
			return d;
		} else {
			return '';
		}
	}

	$: tickVals = Array.isArray(ticks) ? ticks : $yScale.ticks(tickNumber);
</script>

<g class='axis y-axis' transform='translate(-{$padding.left}, 0)'>
	{#each tickVals as tick, i}
		{#if shouldDisplay(tick)}
		<g class='tick tick-{tick}' transform='translate(0, {$yScale(tick)})'>
			{#if gridlines !== false}
				<line x2='100%'></line>
			{/if}
			<text y='-4'>{formatTick(tick)}</text>
		</g>
		{/if}
	{/each}
</g>

<style>
	.tick {
		font-size: .725em;
		font-weight: 200;
	}

	.tick line {
		stroke: #aaa;
		stroke-dasharray: 2;
	}

	.tick text {
		fill: #666;
		text-anchor: start;
	}

	.tick.tick-0 line {
		stroke-dasharray: 0;
	}
</style>
