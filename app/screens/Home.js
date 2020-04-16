import React from 'react'

export default () => {
  const img = <img src="/imgs/party-blob.gif" className="p-2" />
  return (
    <div className="home-hero text-gray-700 font-bold">
      <div>
        <div className="smaller">Are you ready to</div>
        <div>Gif The</div>
        <div className="text-rainbow">
          {['F', 'U', 'N', 'K'].map(l => <span key={l}>{l}</span>)}
        </div>
      </div>
      <div>Out?</div>
      <a href="#/image/new/" className="text-blue-500 flex items-center justify-center ">
        {img} Heck Yeah! {img}
      </a>
    </div>
  )
}