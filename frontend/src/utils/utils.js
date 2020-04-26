export default function formatNumber(cur) {
  let formatValue = cur.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return formatValue;
}
