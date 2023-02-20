export default function capitalise(str) {
  return str.replace(/\b\w/g, function (l) {
    return l.toUpperCase();
  });
}
