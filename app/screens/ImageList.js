import React from 'react'
import RestHook from '@unrest/react-api'
import ImageCard from '../components/ImageCard'

const withImages = RestHook('/api/server/SourceImage/')


const BaseImageList = props => {
  const { loading, results=[] } = props.api
  if (loading) {
    return null
  }
  return (
    <div>
      <h1 className="h1 text-center">Select an Image to Partify</h1>
      <div className="flex flex-wrap justify-center">
        {results.map(({id, name, src}) => (
          <ImageCard key={id} to={`/image/${id}/`} src={src}>
            <div className="text-center mb-4">{name}</div>
          </ImageCard>
        ))}
      </div>
    </div>
  )
}

export default withImages(BaseImageList)