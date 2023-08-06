import { Panel } from "../../core/layout/side_panel";
import { Size, Layoutable } from "../../core/layout";
import { SerializableState } from "../../core/view";
import { Renderer, RendererView } from "../renderers/renderer";
import { ColumnarDataSource } from "../sources/columnar_data_source";
export declare abstract class AnnotationView extends RendererView {
    model: Annotation;
    layout?: Layoutable;
    panel?: Panel;
    update_layout?(): void;
    after_layout?(): void;
    get_size(): Size;
    protected _get_size(): Size;
    connect_signals(): void;
    set_data(source: ColumnarDataSource): void;
    get needs_clip(): boolean;
    serializable_state(): SerializableState;
}
export declare namespace Annotation {
    type Attrs = Renderer.Attrs;
    type Props = Renderer.Props;
    type Visuals = Renderer.Visuals;
}
export interface Annotation extends Annotation.Attrs {
}
export declare abstract class Annotation extends Renderer {
    properties: Annotation.Props;
    __view_type__: AnnotationView;
    constructor(attrs?: Partial<Annotation.Attrs>);
    static init_Annotation(): void;
}
//# sourceMappingURL=annotation.d.ts.map