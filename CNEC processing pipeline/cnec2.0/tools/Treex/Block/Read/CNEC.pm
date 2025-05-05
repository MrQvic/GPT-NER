package Treex::Block::Read::CNEC;
use Moose;
use Treex::Core::Common;
extends 'Treex::Block::Read::BaseTextReader';

use HTML::Entities qw(decode_entities);

sub _process_sentence {
  my ($self, $document, $sentence) = @_;

  return if not $sentence;

  my $bundle = $document->create_bundle();
  my $zone = $bundle->create_zone( $self->language, $self->selector );
  my $a_root = $zone->create_atree();
  my $n_root = $zone->create_ntree();

  my @a_nodes = ();
  my @stack = {node=>$n_root};
  while ($sentence) {
    if ($sentence =~ s/^>\s*//) {
      log_fatal "Closing named entity which is not closed when parsing $sentence" if @stack <= 1;
      my @entity_a_nodes = @a_nodes[$stack[-1]->{start} .. $#a_nodes];
      $stack[-1]->{node}->set_anodes(@entity_a_nodes);
      $stack[-1]->{node}->set_normalized_name(join ' ', map { $_->form } @entity_a_nodes);
      pop @stack;
    } elsif ($sentence =~ s/^<([^<\s]+)\s*//) {
      push @stack, {node=>$stack[-1]->{node}->create_child(ne_type=>$1), start=>scalar(@a_nodes)};
    } elsif ($sentence =~ s/^([^\s<>]+)\s*//) {
      push @a_nodes, $a_root->create_child(form => decode_entities($1), ord => @a_nodes + 1);
    } else {
      log_fatal "Cannot parse $sentence";
    }
  }
}

sub next_document {
    my ($self) = @_;
    my $text = $self->next_document_text();
    return if !defined $text;

    my $document = $self->new_document();
    foreach my $sentence ( split /\n/, $text ) {
        _process_sentence($self, $document, $sentence);
    }

    return $document;
}

1;

__END__

=head1 NAME

Treex::Block::Read::CNEC

=head1 SYNOPSIS

 Read::CNEC from='!dir*/file*.txt'

=head1 DESCRIPTION

Document reader for plain text CNEC (Czech Named Entity Corpus) format.
The files contain one sentence per line, entities are hierarchic and
encoded using <type text> or <type<type text>>.  The sentences are stored into
L<bundles|Treex::Core::Bundle> in the L<document|Treex::Core::Document>.

=head1 ATTRIBUTES

=over

=item from

space or comma separated list of filenames
See L<Treex::Core::Files> for full syntax.

=back

=head1 METHODS

=over

=item next_document

Loads a document.

=back

=head1 SEE

L<Treex::Block::Read::BaseTextReader>
L<Treex::Core::Document>
L<Treex::Core::Bundle>
L<Treex::Block::Read::Sentences>

=head1 AUTHOR

Milan Straka

=head1 COPYRIGHT AND LICENSE

Copyright © 2013 by Institute of Formal and Applied Linguistics, Charles University in Prague

This module is free software; you can redistribute it and/or modify it under the same terms as Perl itself.
