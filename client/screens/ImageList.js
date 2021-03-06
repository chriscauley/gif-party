import React from 'react'
import { Link } from 'react-router-dom'
import RestHook from '@unrest/react-rest-hook'
import auth from '@unrest/react-auth'
import css from '@unrest/css'

import ImageCard from '../components/ImageCard'
import Form from '@unrest/react-jsonschema-form'
import { post } from '@unrest/core'

const withSourceImages = RestHook('/api/server/SourceImage/')

const BaseImageList = (props) => {
  const { loading, items = [] } = props.api
  if (loading) {
    return null
  }
  return (
    <div className="relative">
      <h1 className="h1 text-center">Select an Image to Partify</h1>
      <div className="flex flex-wrap justify-center">
        {items.map(({ id, name, src }) => (
          <ImageCard key={id} to={`/image/${id}/`} src={src}>
            <div className="text-center mb-4">{name}</div>
          </ImageCard>
        ))}
      </div>
      <div className="m-8 fixed bottom-0 right-0">
        <Link
          to="/new/SourceImage/"
          className="rounded-full text-white bg-blue-500 text-3xl w-12 h-12 flex items-center justify-center shadow-2xl"
        >
          <span className="fa fa-plus" />
        </Link>
      </div>
    </div>
  )
}

export default withSourceImages(BaseImageList)

const withSourceImageSchema = RestHook('/api/schema/SourceImage/')

const BaseNewSourceImageModal = (props) => {
  if (props.api.loading) {
    return null
  }
  // TODO onSuccess should use router to avoid page refresh
  return (
    <div className={css.modal.outer()}>
      <Link to={'/images'} className={css.modal.mask()} />
      <div className={css.modal.content()}>
        <Form
          onSubmit={(formData) => post(props.api.post_url, formData)}
          onSuccess={(data) =>
            props.history.replace(`/image/${data.sourceimage_id}/`)
          }
          schema={props.api.schema}
        />
      </div>
    </div>
  )
}

export const NewSourceImageModal = auth.required(
  withSourceImageSchema(BaseNewSourceImageModal),
)
