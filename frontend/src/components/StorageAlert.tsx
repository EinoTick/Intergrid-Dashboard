export default function StorageAlert({ stateOfCharge }: { stateOfCharge: number }) {
  if (stateOfCharge >= 90) {
    return <div className="alert warn">Storage nearly full: {stateOfCharge.toFixed(1)}%</div>
  }
  if (stateOfCharge <= 10) {
    return <div className="alert danger">Storage critically low: {stateOfCharge.toFixed(1)}%</div>
  }
  return <div className="alert">Storage level: {stateOfCharge.toFixed(1)}%</div>
}
