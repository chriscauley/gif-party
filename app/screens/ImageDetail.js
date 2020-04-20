import React from 'react'
import RestHook from '@unrest/react-api'
import Form from '@unrest/react-jsonschema-form'
import { cloneDeep } from 'lodash'

const withImage = RestHook('/api/server/SourceImage/${match.params.object_id}/')
const withImageSchema = RestHook('/api/schema/PartyImage/')

const getSchema = (schema, n_frames, colors) => {
  schema = cloneDeep(schema)

  // gifs already have frame counts and so they can't have more
  if (n_frames > 1) {
    delete schema.properties.n_frames
  }

  // colors are on a gif by gif basis
  schema.properties.replace_color.enum = ['']
  schema.properties.replace_color.enumNames = ['']
  colors.forEach(({color, count}) => {
    schema.properties.replace_color.enum.push(color)
    color = color.replace('srgba', 'rgba')
    schema.properties.replace_color.enumNames.push(`${color} (${count})`)
  })

  return schema
}

const getUISchema = (schema, formData={}) => {
  const uiSchema = {}
  const hide = property => uiSchema[property] = {"classNames": "hidden"}
  if (formData.method !== 'replace') {
    hide('fuzz')
    hide('replace_color')
  } else if (formData.method !== 'hue_rotate') {
    hide('negate')
  }
  return uiSchema
}

// TODO move this to a more general place
const getInitial = schema => {
  const initial = {}
  const { required=[] } = schema
  Object.entries(schema.properties).forEach(([key, field]) => {
    if (field.default !== null && field.default !== undefined) {
      initial[key] = field.default
    } else if (field.enum) {
      initial[key] = field.enum[0]
    }
  })
  return initial
}


const getCSRF = (cookie=document.cookie) => {
  const match = cookie.match(/csrftoken=([^;]+)/)
  return match && match[1]
}


class BaseImageForm extends React.Component {
  state = {
    formData: undefined,
    error: undefined,
  }
  onChange = formData => this.setState({formData})

  submit = formData => {
    const { sourceimage_id } = this.props
    return fetch("/api/party/", {
      body: JSON.stringify({...formData, sourceimage_id}),
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        "X-CSRFToken": getCSRF()
      }
    })
      .then(r => r.json())
      .catch(error => this.setState({error}))
      .then(this.props.onSuccess)
  }

  render() {
    const { api, n_frames, colors } = this.props
    if (api.loading) {
      return null
    }
    const schema = getSchema(api.schema, n_frames, colors, this.state.formData)
    const initial = getInitial(schema)
    return (
      <Form
        schema={schema}
        uiSchema={getUISchema(schema, this.state.formData)}
        initial={initial}
        formData={this.state.formData || initial}
        error={this.state.error}
        onChange={this.onChange}
        onSubmit={this.submit}
      />
    )
  }
}

const ImageForm = withImageSchema(BaseImageForm)

export default withImage(props => {
  const { variants, loading, id, src, name, colors, n_frames, refetch } = props.api
  if (loading && !variants) {
    return null
  }
  return (
    <div className="flex">
      <div className="w-1/3 p-4">
        <ImageForm
          colors={colors}
          n_frames={n_frames}
          onSuccess={() => refetch(props)}
          sourceimage_id={id}
        />
      </div>
      <div className="w-2/3 p-4">
        {variants.map(({src, name}) => (
          <div key={name}>
            <img src={src} />
            {name}
          </div>
        ))}
      </div>
    </div>
  )
})
