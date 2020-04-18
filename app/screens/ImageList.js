import React from 'react'
import { Link } from 'react-router-dom'
import RestHook from '@unrest/react-api'

const withImages = RestHook('/api/server/SourceImage/')

const css = {
  wrapper: "flex flex-wrap",
  card_outer: "w-full sm:w-1/3 p-4",
  card: "border rounded p-4 text-center block",
  img: "list-img bg-gray-100",
}


const BaseImageList = props => {
  const { loading, results=[] } = props.api
  if (loading) {
    return null
  }
  return (
    <div className={css.wrapper}>
      {results.map(({id, name, src}) => (
        <div key={id} className={css.card_outer}>
          <Link to={`/image/${id}/`} className={css.card}>
            <div className={css.img}>
              <img src={src} />
            </div>
            <div>{name}</div>
          </Link>
        </div>
      ))}
    </div>
  )
}

export default withImages(BaseImageList)