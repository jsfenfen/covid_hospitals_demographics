<script>
  import { getContext } from 'svelte';
  import * as geo from 'd3-geo';

  const { data, width, height } = getContext('LayerCake');

  export let projectionName = 'geoAlbersUsa';
  export let fill_mapping;
  export let name;

  /* --------------------------------------------
   * Add this in case you want to plot only a subset of the features
   * while keeping the zoom on the whole geojson feature set
   */
  export let features = $data.features;

  $: projection = geo[projectionName]()
    .fitSize([$width, $height], $data);

  $: geoPath = geo.geoPath(projection);

  function set_fill(key) {
    return fill_mapping[key];
  }

</script>

<g class="map-group">
  {#each features as feature}
    <path
      class="feature-path"
      fill="{set_fill(feature.id)}"
      d="{geoPath(feature)}"
    ></path>
  {/each}
</g>

<style>
  .feature-path {
    stroke: #999;
    stroke-width: 0.5px;
  }
</style>