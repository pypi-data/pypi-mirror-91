import { TextAnnotation, TextAnnotationView } from "./text_annotation";
import { FontStyle, VerticalAlign, TextAlign, TextBaseline } from "../../core/enums";
import { Size, Layoutable } from "../../core/layout";
import { Panel } from "../../core/layout/side_panel";
import * as mixins from "../../core/property_mixins";
import * as p from "../../core/properties";
export declare class TitleView extends TextAnnotationView {
    model: Title;
    visuals: Title.Visuals;
    layout: Layoutable;
    panel: Panel;
    initialize(): void;
    protected _get_location(): [number, number];
    protected _render(): void;
    protected _get_size(): Size;
}
export declare namespace Title {
    type Attrs = p.AttrsOf<Props>;
    type Props = TextAnnotation.Props & {
        text: p.Property<string>;
        text_font: p.Property<string>;
        text_font_size: p.StringSpec;
        text_font_style: p.Property<FontStyle>;
        text_color: p.ColorSpec;
        text_alpha: p.NumberSpec;
        text_line_height: p.Property<number>;
        vertical_align: p.Property<VerticalAlign>;
        align: p.Property<TextAlign>;
        offset: p.Property<number>;
        standoff: p.Property<number>;
        text_align: p.Property<TextAlign>;
        text_baseline: p.Property<TextBaseline>;
    } & Mixins;
    type Mixins = mixins.BorderLine & mixins.BackgroundFill;
    type Visuals = TextAnnotation.Visuals;
}
export interface Title extends Title.Attrs {
}
export declare class Title extends TextAnnotation {
    properties: Title.Props;
    __view_type__: TitleView;
    constructor(attrs?: Partial<Title.Attrs>);
    static init_Title(): void;
}
//# sourceMappingURL=title.d.ts.map