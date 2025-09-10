import {useState} from 'react';

function App() {

  const [address, setAddress] = useState("")
  const [distance, setDistance] = useState("")

  function handleAddressChange(event){
    setAddress(e => event.target.value)
  }

  function handleDistanceChange(event){
    let val = event.target.value 
    if (val > 31){
      val = 31
    }
    else if(distance < 0){
      val = 0
    }
    setDistance(e => val)
  }

  function handleButtonClick(){
    //check fields to see if they're empty
    //call the backend for the bar search function + pass address, distance
    //if search returns 0 put in a popup window explaining error
    //else go to winwheel page
    console.log({address})
    console.log({distance})
  }

  return (
      <div>
        <h1>Bar Roulette</h1>
        <p>Welcome to Bar Roulette</p><br></br>
        <input type="text" value={address} onChange={handleAddressChange} placeholder='Address'></input><br></br>
        <input type="number" min={0} max={31} value={distance} onChange={handleDistanceChange} placeholder='Distance'></input><br></br>
        <button onClick={handleButtonClick}>SPIN</button>
      </div>
  )
}

export default App
