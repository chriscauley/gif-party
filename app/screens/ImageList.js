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
    <div className="flex flex-wrap">
      {results.map(({id, name, src}) => (
        <ImageCard key={id} to={`/image/${id}/`} src={src}>
          <div className="text-center mb-4">{name}</div>
        </ImageCard>
      ))}
    </div>
  )
}

export default withImages(BaseImageList)