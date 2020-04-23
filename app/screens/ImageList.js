import React from 'react'
import RestHook from '@unrest/react-rest-hook'
import css from '@unrest/css'

import ImageCard from '../components/ImageCard'
import Modal from '../components/Modal'
import Form, { post } from '@unrest/react-jsonschema-form'

const withSourceImages = RestHook('/api/server/SourceImage/')

const BaseImageList = (props) => {
  const { loading, results = [] } = props.api
  if (loading) {
    return null
  }
  return (
    <div className="relative">
      <h1 className="h1 text-center">Select an Image to Partify</h1>
      <div className="flex flex-wrap justify-center">
        {results.map(({ id, name, src }) => (
          <ImageCard key={id} to={`/image/${id}/`} src={src}>
            <div className="text-center mb-4">{name}</div>
          </ImageCard>
        ))}
      </div>
      <div className="m-8 fixed bottom-0 right-0">
        <a href="#/new/SourceImage/" className='rounded-full text-white bg-blue-500 text-3xl w-12 h-12 flex items-center justify-center shadow-2xl'>
          <span className="fa fa-plus"/>
        </a>
      </div>
    </div>
  )
}

export default withSourceImages(BaseImageList)

const withSourceImageSchema = RestHook('/api/schema/SourceImage/')

export const NewSourceImageModal = withSourceImageSchema(props => {
  if (props.api.loading) { return null }
  // TODO onSuccess should use router to avoid page refresh
  return (
    <Modal>
      <Form
        onSubmit={formData => post(props.api.post_url, formData)}
        onSuccess={data => window.location = `/image/${data.sourceimage_id}/`}
        schema={props.api.schema}
      />
    </Modal>
  )
})
